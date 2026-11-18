/** @odoo-module **/
/* global window */

import {App, useRef, whenReady} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {makeEnv, startServices} from "@web/env";
import SignOcaPdf from "../sign_oca_pdf/sign_oca_pdf.esm.js";
import {getTemplate} from "@web/core/templates";
import {MainComponentsContainer} from "@web/core/main_components_container";
import {rpc} from "@web/core/network/rpc";
import {startSignItemNavigator} from "./sign_oca_navigator.esm";

export class SignOcaPdfPortal extends SignOcaPdf {
    setup() {
        this.rpc = rpc;
        this.signOcaFooter = useRef("sign_oca_footer");
        this.signer_id = this.props.signer_id;
        this.access_token = this.props.access_token;
        super.setup(...arguments);
    }
    async willStart() {
        this.info = await this.rpc(
            "/sign_oca/info/" + this.signer_id + "/" + this.access_token
        );
    }
    getPdfUrl() {
        return "/sign_oca/content/" + this.signer_id + "/" + this.access_token;
    }
    checkToSign() {
        this.to_sign = this.to_sign_update;
        if (this.to_sign_update) {
            this.signOcaFooter.el.style.display = "";
            const button = document.getElementById("sign_oca_button");
            if (button) {
                button.removeAttribute("disabled");
            }
        } else {
            this.signOcaFooter.el.style.display = "none";
            const button = document.getElementById("sign_oca_button");
            if (button) {
                button.disabled = true;
            }
        }
    }
    postIframeFields() {
        super.postIframeFields(...arguments);
        this.checkFilledAll();
        // Is essential to make sure the navigator will never duplicate
        const doc = this.iframe.el.contentDocument;
        const target = doc.getElementById("viewerContainer");
        const navigator = doc.getElementsByClassName(
            "o_sign_sign_item_navigator"
        );
        const navLine = doc.getElementsByClassName("o_sign_sign_item_navline");
        if (navLine.length === 0) {
            const line = doc.createElement("div");
            line.classList.add("o_sign_sign_item_navline");
            target.append(line);
        }
        if (navigator.length === 0) {
            const nav = doc.createElement("div");
            nav.classList.add("o_sign_sign_item_navigator");
            target.append(nav);
        }
        // Load navigator
        this.navigate();
    }
    async _onClickSign(ev) {
        ev.target.disabled = true;
        const position = await this.getLocation();
        this.rpc("/sign_oca/sign/" + this.signer_id + "/" + this.access_token, {
            items: this.info.items,
            latitude: position && position.coords && position.coords.latitude,
            longitude: position && position.coords && position.coords.longitude,
        }).then((action) => {
            // As we are on frontend env, it is not possible to use do_action(), so we
            // redirect to the corresponding URL or reload the page if the action is not
            // an url.
            if (action.type === "ir.actions.act_url") {
                window.location = action.url;
            } else {
                window.location.reload();
            }
        });
    }
    navigate() {
        const target = this.iframe.el.contentDocument.getElementById("viewerContainer");
        this.navigator = startSignItemNavigator(this, target, this.env);
    }
}
SignOcaPdfPortal.template = "sign_oca.SignOcaPdfPortal";
SignOcaPdfPortal.props = {
    access_token: String,
    signer_id: Number,
};
SignOcaPdfPortal.components = {MainComponentsContainer};

export async function initDocumentToSign(document, sign_oca_backend_info) {
    const env = makeEnv();
    await startServices(env);
    await whenReady();
    const app = new App(SignOcaPdfPortal, {
        getTemplate,
        env: env,
        dev: env.debug,
        props: {
            access_token: sign_oca_backend_info.access_token,
            signer_id: sign_oca_backend_info.signer_id,
        },
        translateFn: _t,
        translatableAttributes: ["data-tooltip"],
    });
    await app.mount(document.body);
}
export default {SignOcaPdfPortal, initDocumentToSign};
