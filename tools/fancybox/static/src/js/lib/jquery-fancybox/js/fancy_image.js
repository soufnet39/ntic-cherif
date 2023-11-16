// Copyright 2017 - 2018 Modoolar <info@modoolar.com>
// License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

odoo.define('web_widget_fancy.FancyTemplate', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var registry = require('web.field_registry');
    var _t = core._t;

    var UrlImage = AbstractField.extend({
        className: 'o_attachment_image',
        template: 'FancyTemplate',
        placeholder: "/web/static/src/img/placeholder.png",
        supportedFieldTypes: ['char'],

        url: function () {
            return this.value ? this.value : this.placeholder;
        },

        _render: function () {
            this._super(arguments);

            var self = this;
            var $img = this.$("img:first");
            $img.attr('src', $img[0].src+"?t="+Date.now() );
            $img.on('error', function () {
                $img.attr('src', self.placeholder);
                // self.do_warn(
                //     _t("Image"), _t("Could not display the selected image."));
            });
        },
    });

    registry.add('fancy', UrlImage);
});
