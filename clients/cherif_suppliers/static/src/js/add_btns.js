odoo.define('cherif_suppliers.new_buttons', function (require) {
"use strict";
var core = require('web.core');
var _t = core._t;
var ListController = require('web.ListController');

    ListController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.find('.oe_recap_suppliers').off().click(this.proxy('call_recap_suppliers'));

            }
        },
        call_recap_suppliers: function () {

            var self = this;

                self.do_action({
                    type: "ir.actions.act_window",
                    name: _t("Mis à jour des opérations"),
                    res_model: "cherif_suppliers.suivi_wizard",
                    views: [[false,'form']],
                    target: 'current',
                    view_mode : 'form',
                    context: {'form_view_ref': 'cherif_suppliers.suivi_wizard_form'},
                    flags: {'form': {'action_buttons': true, 'options': 
                        {
                            'mode': 'edit'                        
                        }}}
                });
   
           

        }

    });

  

})
