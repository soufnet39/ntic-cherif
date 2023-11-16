from odoo import api, models
class ReportAttendanceRecap(models.AbstractModel):
    _name = 'report.sn_invoices.facture_report'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('sn_invoices.facture_report')
        docs_ctn = self.env['sn_invoices.invoices'].browse(docids)
        docargs =  {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs_ctn,

        }
        return docargs