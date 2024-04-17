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

odoo.define('sn_base.WebClient', function (require) {

  "use strict";
  
      var AbstractWebClient = require('web.AbstractWebClient');
  
      AbstractWebClient = AbstractWebClient.include({
  
          start: function (parent) {
  
              var ee= require('web.session');
              this.set('title_part', {"zopenerp": ee.db.charAt(0).toUpperCase() + ee.db.slice(1)
             });
              
  
              this._super(parent);
  
          },
  
      });
  
  });