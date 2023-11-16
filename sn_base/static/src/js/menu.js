odoo.define('sn_base.ComplementMenu', function(require) {
"use strict";
var core = require('web.core');
var Dialog = require('web.Dialog');
var _t = core._t;
var QWeb = core.qweb;
var UserMenu = require('web.UserMenu');

var ComplementMenu = UserMenu.include({
    _onMenuAbout: function () {

    new Dialog(this, {
            size: 'large',
            dialogClass: 'o_act_window',
            title: _t("A propos de nous.."),
            $content: $(QWeb.render("Ntix.about"))
        }).open();

    },
  });
return ComplementMenu;
});