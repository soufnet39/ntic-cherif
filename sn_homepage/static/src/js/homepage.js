odoo.define('sn_homepage.homepage', function (require) {
"use strict";

var core = require('web.core');
var framework = require('web.framework');
var session = require('web.session');
var ajax = require('web.ajax');
var ActionManager = require('web.ActionManager');
var view_registry = require('web.view_registry');
var Widget = require('web.Widget');
var AbstractAction = require('web.AbstractAction');
var ControlPanelMixin = require('web.ControlPanelMixin');
var QWeb = core.qweb;

var _t = core._t;
var _lt = core._lt;
var HrHomepageView = AbstractAction.extend(ControlPanelMixin, {
 events: {

        //'click .timesheet': 'action_timesheet_user',
        //'click .my_profile': 'action_my_profile',
	},
	init: function(parent, context) {
        this._super(parent, context);
        var employee_data = [];
        var self = this;
        if (context.tag == 'sn_homepage.homepage') {
            self._rpc({
                model: 'sn_homepage.homepage',
                method: 'get_employee_info',
            }, []).then(function(result){
            console.log(result)
                self.data = result
            }).done(function(){
                self.render();
                self.href = window.location.href;
            });
        }
    },
    willStart: function() {
         return $.when(ajax.loadLibs(this), this._super());
    },
    start: function() {
        var self = this;
        return this._super();
    },
    render: function() {
        var super_render = this._super;
        var self = this;
        var hr_homepage = QWeb.render( 'sn_homepage.homepage', {
            widget: self,
        });
        $( ".o_control_panel" ).addClass( "o_hidden" );
        $(hr_homepage).prependTo(self.$el);


        return hr_homepage
    },
    reload: function () {
            window.location.href = this.href;
    },

    });
core.action_registry.add('sn_homepage.homepage', HrHomepageView);
return HrHomepageView
});
