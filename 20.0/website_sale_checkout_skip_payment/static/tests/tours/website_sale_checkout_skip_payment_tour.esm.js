import * as tourUtils from "@website_sale/js/tours/tour_utils";
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("website_sale_checkout_skip_payment", {
    url: "/shop",
    steps: () => [
        {
            content: "Navigate from the homepage to the shop",
            trigger: "#top_menu a[href='/shop']",
            run: "click",
            expectUnloadPage: true,
        },
        ...tourUtils.searchProduct("Test Product", {select: true}),
        ...tourUtils.addToCartFromProductPage(),
        tourUtils.goToCart({quantity: 1}),
        tourUtils.goToCheckout(),
        tourUtils.confirmOrder(),
        {
            content: "Confirm without payment",
            trigger:
                "#skip_payment_method button[name='o_payment_submit_button']",
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: "Print order",
            trigger: "a[href='/shop/print']",
        },
    ],
});
