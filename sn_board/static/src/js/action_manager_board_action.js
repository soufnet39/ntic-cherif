odoo.define('board.ActionManager', function (require) {
"use strict";

/**
 * The purpose of this file is to patch the ActionManager to properly generate
 * the flags for the 'ir.actions.act_window' of model 'sn_board.board'.
 */

var ActionManager = require('web.ActionManager');

ActionManager.include({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     * @private
     */
    _executeWindowAction: function (action) {
        if (action.res_model === 'sn_board.board' && action.view_mode === 'form') {
            action.target = 'inline';
            _.extend(action.flags, {
                hasSearchView: false,
                hasSidebar: false,
                headless: true,
            });
        }
        return this._super.apply(this, arguments);
    },
});

});
