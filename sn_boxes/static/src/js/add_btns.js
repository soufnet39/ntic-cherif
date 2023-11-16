odoo.define('sn_boxes.new_buttons', function (require) {
"use strict";
var ListController = require('web.ListController');
    ListController.include({
        renderButtons: function($node) {

        this._super.apply(this, arguments);
            if (this.$buttons) {

               this.$buttons.find('.oe_sold_in_button').off().click(this.proxy('call_sold_in'));
            }
        },
        call_sold_in: function () {
                   this.do_action({
                        type: "ir.actions.act_window",
                        name: "Encaissement",
                        res_model: "sn_boxes.operations",
                        views: [[false,'form']],
                        target: 'current',
                        view_mode : 'form',
                        context:    '{"default_operation":"reception","default_sens":"credit"}',
                        flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
                    });
        }

    });
    ListController.include({
        renderButtons: function($node) {
        this._super.apply(this, arguments);
            if (this.$buttons) {
               this.$buttons.find('.oe_sold_out_button').off().click(this.proxy('call_sold_out'));
            }
        },
        call_sold_out: function () {
                   this.do_action({
                        type: "ir.actions.act_window",
                        name: "Décaissement",
                        res_model: "sn_boxes.operations",
                        views: [[false,'form']],
                        target: 'current',
                        view_mode : 'form',
                        context:    '{"default_operation":"degagement","default_sens":"debit"}',
                        flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
                    });

        }

    });
    ListController.include({
        renderButtons: function($node) {
        this._super.apply(this, arguments);
            if (this.$buttons) {
               this.$buttons.find('.oe_between_boxes_button').off().click(this.proxy('call_between_boxes'));
            }
        },
        call_between_boxes: function () {
                   this.do_action({
                        type: "ir.actions.act_window",
                        name: "Entre caisses",
                        res_model: "sn_boxes.interboxes",
                        views: [[false,'form']],
                        target: 'inline',
                        view_mode : 'form',
                        flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
                    });

        }

    });



})
