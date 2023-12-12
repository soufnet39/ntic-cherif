odoo.define('cherif.new_buttons', function (require) {
"use strict";
var core = require('web.core');
var _t = core._t;
var ListController = require('web.ListController');

    ListController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.find('.oe_black_list').off().click(this.proxy('call_maj_black_list'));

            }
        },
        call_maj_black_list: function () {

            var self = this;
            self.do_action({
                type: "ir.actions.act_window",
                name: _t("Mis à jour de la liste noire"),
                res_model: "cherif.black_list_wizard",
                views: [[false,'form']],
                target: 'current',
                view_mode : 'form',
                context: {'form_view_ref': 'cherif.black_list_wizard_form'},
                flags: {'form': {'action_buttons': true, 'options': 
                    {
                        'mode': 'edit'                        
                    }}}
            });
   
           

        }

    });

  

})
