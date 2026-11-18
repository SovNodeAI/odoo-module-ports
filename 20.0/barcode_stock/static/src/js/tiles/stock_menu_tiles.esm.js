import {_t} from "@web/core/l10n/translation";
import {barcodeMenuTiles} from "@barcode_scanner/js/registries.esm";

/**
 * Home-screen tiles for stock. Isolated in its own file so it can be moved to
 * `barcode_stock` untouched in phase 2.
 */

barcodeMenuTiles.add(
    "warehouse_ops",
    {
        label: _t("Warehouse Operations"),
        icon: "home",
        iconClass: "ilx-icon-warehouse",
        action: ({navigate}) => navigate("warehouse_ops"),
    },
    {sequence: 10}
);

barcodeMenuTiles.add(
    "internal_transfer",
    {
        label: _t("Internal Transfer"),
        icon: "swap_horiz",
        iconClass: "ilx-icon-transfer",
        action: ({navigate}) => navigate("internal_transfer"),
    },
    {sequence: 20}
);

barcodeMenuTiles.add(
    "quick_info",
    {
        label: _t("Quick Info"),
        icon: "info",
        iconClass: "ilx-icon-info",
        action: ({navigate}) => navigate("quick_info"),
    },
    {sequence: 30}
);
