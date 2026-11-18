import {Component, proxy, t, useProps} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";

export class SocialImageDialog extends Component {
    static template = "social_media_base.SocialImageDialog";
    props = useProps({
        images: t.array(t.string()),
        title: t.string().optional(),
        fullscreen: t.boolean().optional(),
        close: t.function().optional(),
    });
    static components = {
        Dialog,
    };

    /** @override */
    setup() {
        super.setup();
        this.state = proxy({
            imageUrlActive: this.props.images[0],
        });
    }

    indexImageActive(prev = false, next = false) {
        let currentIndex = this.props.images.indexOf(this.state.imageUrlActive);
        if (prev) {
            currentIndex =
                (currentIndex === 0 ? this.props.images.length : currentIndex) - 1;
        } else if (next) {
            currentIndex = (currentIndex + 1) % this.props.images.length;
        }
        return this.props.images[currentIndex];
    }

    prevImage() {
        this.state.imageUrlActive = this.indexImageActive(true);
    }

    nextImage() {
        this.state.imageUrlActive = this.indexImageActive(false, true);
    }
}
