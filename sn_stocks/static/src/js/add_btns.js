odoo.define('sn_stocks.new_buttons', function (require) {
"use strict";
var ListController = require('web.ListController');

    ListController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.find('.oe_bon_livraison_button').off().click(this.proxy('call_bon_livraison'));

            }
        },
        call_bon_livraison: function () {

            var self = this;
            self._rpc({
                model: 'ir.model.data',
                method: 'xmlid_to_res_id',
                kwargs: { xmlid: 'sn_stocks.stocks_operation_form' },
            }).then(function (res_id) {
                self.do_action({
                    type: "ir.actions.act_window",
                    name: "Bon de livraison",
                    res_model: "sn_sales.commandes",
                    views: [[res_id,'form']],
                    target: 'current',
                    view_mode : 'form',
                    context:    '{"default_document_type":"livraison"}',
                    flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
                });
            })

        }

    });

    ListController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.find('.oe_bon_reception_button').off().click(this.proxy('call_bon_reception'));

            }
        },
        call_bon_reception: function () {

            var self = this;
            self._rpc({
                model: 'ir.model.data',
                method: 'xmlid_to_res_id',
                kwargs: { xmlid: 'sn_stocks.stocks_operation_form' },
            }).then(function (res_id) {
                self.do_action({
                    type: "ir.actions.act_window",
                    name: "Bon de reception",
                    res_model: "sn_sales.commandes",
                    views: [[res_id,'form']],
                    target: 'current',
                    view_mode : 'form',
                    context:    '{"default_document_type":"reception"}',
                    flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
                });
            })

        }

    });

    ListController.include({

        renderButtons: function($node) {
        this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.find('.oe_bon_sortie_button').off().click(this.proxy('call_bon_sortie'));
            }
        },
        call_bon_sortie: function () {

            var self = this;
            self._rpc({
                model: 'ir.model.data',
                method: 'xmlid_to_res_id',
                kwargs: { xmlid: 'sn_stocks.stocks_operation_form' },
            }).then(function (res_id) {
                self.do_action({
                    type: "ir.actions.act_window",
                    name: "Bon de Sortie",
                    res_model: "sn_sales.commandes",
                    views: [[res_id,'form']],
                    target: 'current',
                    view_mode : 'form',
                    context:    '{"default_document_type":"sortie"}',
                    flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
                });
            })

        }

    });

    ListController.include({
        renderButtons: function($node) {
        this._super.apply(this, arguments);
            if (this.$buttons) {
               this.$buttons.find('.oe_bon_entree_button').off().click(this.proxy('call_bon_entree'));
            }
        },
        call_bon_entree: function () {

            var self = this;
            self._rpc({
                model: 'ir.model.data',
                method: 'xmlid_to_res_id',
                kwargs: { xmlid: 'sn_stocks.stocks_operation_form' },
            }).then(function (res_id) {
                self.do_action({
                    type: "ir.actions.act_window",
                    name: "Bon d'Entrée",
                    res_model: "sn_sales.commandes",
                    views: [[res_id,'form']],
                    target: 'current',
                    view_mode : 'form',
                    context:    '{"default_document_type":"entree"}',
                    flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
                });
            })

        }

    });

    ListController.include({
        renderButtons: function($node) {
        this._super.apply(this, arguments);
            if (this.$buttons) {
               this.$buttons.find('.oe_between_stocks_button').off().click(this.proxy('call_between_stocks'));
            }
        },
        call_between_stocks: function () {
                   this.do_action({
                        type: "ir.actions.act_window",
                        name: "Entre Stocks",
                        res_model: "sn_stocks.interstocks",
                        views: [[false,'form']],
                        target: 'inline',
                        view_mode : 'form',
                        flags: {'form': {'action_buttons': false,
                                         'options': {'mode': 'edit'}}}
                    });
                    return {
                            'type': 'ir.actions.client',
                            'tag': 'reload',
                    }
        }

    });

})
