odoo.define('sn_expenses.new_buttons', function (require) {
"use strict";
var ListController = require('web.ListController');

    ListController.include({
        renderButtons: function($node) {
        this._super.apply(this, arguments);
            if (this.$buttons) {
               this.$buttons.find('.oe_new_expense_button').off().click(this.proxy('call_new_expense'));
            }
        },
        call_new_expense: function () {

                   this.do_action({
                        type: "ir.actions.act_window",
                        name: "Nouvelle Dépense",
                        res_model: "sn_boxes.operations",
                        views: [[false,'form']],
                        target: 'current',
                        view_mode : 'form',
                        context:    "{'default_operation':'expense', 'default_sens':'debit'}",
                        flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
                    });

        }

    });

})
