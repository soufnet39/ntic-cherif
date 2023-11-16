from odoo import api, fields, models
import datetime 

#@########################################################@
class NticEtat104Wiz(models.TransientModel):
    _name = 'sn_invoices.etat_104.wiz'
         
    annee = fields.Integer(string='Anneé')
    invoices_ids = fields.One2many('sn_invoices.etat_104', 'annee', compute="get_factures"  )

    @api.onchange('annee')
    def get_factures(self):
        conditions = [('annee', '=', -1)]

        if self.annee>2017:
            conditions = [('annee', '=', self.annee)]
       
        self.invoices_ids = self.env['sn_invoices.etat_104'].search(conditions)

    def print_etat_104(self):
        return self.env.ref('sn_invoices.etat_104').report_action(self) 

    def export_xlsx_etat_104(self):
        return self.env.ref('sn_invoices.xlsx_etat_104').report_action(self) 

class Etat104Xlsx(models.AbstractModel):
        _name = 'report.sn_invoices.xlsx_etat_104'
        _inherit = 'report.report_xlsx.abstract'
        _description = ''

        ## OVERWITTEN IN ALBELT

        @api.model      
        def generate_xlsx_report(self, workbook, data, etat104):

            for obj in etat104:
                report_name = "Etat 104"
                sheet = workbook.add_worksheet(report_name)
               
                bold = workbook.add_format({'bold': True})
                f_format = workbook.add_format()
                f_format.set_num_format('#,##0.00')

                d_format = workbook.add_format({'num_format': 'YYYY-mm-dd'})
                bold = workbook.add_format({'bold': True})
                sheet.write(0, 0, "sn_invoices",bold)
               # sheet.write(1, 0, "E.U.R.L Hydro Yousfi",bold)
                sheet.write(3, 0, "Etat 104",bold)
                
                headers= [                    				 	
                    "Client",
                    "Adresse",
                    "Reg.Com.",
                    "Mat.Fisc.",
                    "Nis",
                    "Art.Imp.",
                    "HT",
                    "TVA"
                ]
                champs=[
                    "nom",
                    "adresse",
                    "reg_com",
                    "mat_fisc",
                    "nis",
                    "art_imp",
                    "ht",
                    "tva"
                ]
                sheet.write_row(5, 0, headers,bold)
                i=6
                #lines= self.env['sn_invoices.etat_104'].read(obj.invoices_ids)
                #sheet.write(6,0,len(obj.invoices_ids))
                for rw in obj.invoices_ids.read():
                    j=0
                    for ch in champs:    
                        if ch in ['ht','tva']:
                            sheet.write(i, j, rw[ch] or '', f_format)
                        else:
                            sheet.write(i, j, rw[ch] or '')
                        j=j+1
                    i = i + 1

