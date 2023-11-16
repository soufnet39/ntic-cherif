from odoo import api, fields, models,_
from odoo.exceptions import UserError
import itertools

class SnVariantsProducts(models.Model):
    _inherit = 'sn_sales.product'
    _parent_name = "parent_id"
    _parent_store = True
    
    product_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('variants', 'Produit varié'),
        ('composed', 'Produit composé')], 
        string='Product Type', default='consu', required=True,
        help='A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.\n'
             'A variants product is a product with childs of products generated depending of its kind of variants.\n'
             'A composed product is a product with childs of simple products.\n'             
             )
    
    has_variants = fields.Boolean("Avec Variantes", compute='_compute_has_variants' )
    nbr_variants_total = fields.Integer("Avec Variantes", compute='_compute_nbr_variants' )
    nbr_variants_active = fields.Integer("Avec Variantes", compute='_compute_nbr_variants' )
    variants_ids = fields.One2many('sn_variants.categories', 'product_id', string='Variantes',  )
    product_abrv = fields.Char("Abréviation")
    parent_id = fields.Many2one('sn_sales.product', 'Parent', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('sn_sales.product', 'parent_id', 'Child Product')
    
    @api.depends('variants_ids')
    def _compute_has_variants(self):
        for record in self:
            record.has_variants = len(record.variants_ids)>0
           
    @api.depends('child_ids')
    def _compute_nbr_variants(self):
        for record in self:
            record.nbr_variants_total = len(record.child_ids)
            record.nbr_variants_active = 0 #record.child_ids.search_count([('active','=',True)])

            
            

        
    def generate_variants(self):
        kinds=[]
        abrvs=[]
        onsr=[]
        onsr_names=[]
        for v in self.variants_ids:
            # to get something like this: [{'R': 'couleur:rouge', 'V': 'couleur:vert'} , ....]
            kinds.append(v.items_ids.mapped(lambda x: v.display_name+":"+x.name))
            #to get like this: [['V', 'R'], ....]
            abrvs.append(v.items_ids.mapped('item_abrv'))
        if kinds:
            for v in itertools.product(*abrvs) :
                onsr.append('_'.join(map(str,v)) )
            for v in itertools.product(*kinds) :
                onsr_names.append(', '.join(map(str,v)) )

        new_lines=[]
        i=0
        for v in onsr:
            new_child = self.copy()
            new_child["name"] = self.name + ' '+ onsr_names[i] 
            new_child["product_abrv"] = self.product_abrv+'_'+v
            new_child["code"] = self.product_abrv+'_'+v
            new_child["parent_id"] = self.id 
            new_child["product_type"] = 'consu'

            new_lines.append((0, 0, new_child))
            i+=1
        self.env["sn_sales.product"].update(new_lines)
            
     