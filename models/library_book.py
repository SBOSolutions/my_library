# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta

class LibraryBook(models.Model):
    _name = 'library.book'  # this is the most important attibut because it's the name of the database table in that case it will be: library_book
    _description = 'Library Book' # this attibute is used for description
    _order = 'date_release desc, name' # this is a attibute for order by purpose
    _rec_name = 'short_name' # with this attibute you can specify an other field that name for the record representation (this is the name use by the Odoo GUI to represent the record and not the ID in the database table)

    name = fields.Char('Title', required=True)
    short_name = fields.Char(string='Short Title', required = True, translate = True, index = True)
    author_ids = fields.Many2many('res.partner', string='Authors')
    notes = fields.Text(string='Internal Notes')
    state = fields.Selection([
        ('draft', 'Not Available'),
        ('available', 'Available'),
        ('lost', 'Lost')        
    ], string='State', default="draft")
    description = fields.Html(string='Description', sanitize = True, strip_style = False)
    cover = fields.Binary(string='Book Cover')
    out_of_print = fields.Boolean(string='Out of Print ?')
    date_release = fields.Date('Release Date')
    date_updated = fields.Datetime(string='Last Updated')
    pages = fields.Integer(string='Number of pages',
            groups='base.group_user',
            states={'lost': [('readonly', True)]},
            help='Total book page count', company_dependent=False)
    reader_rating = fields.Float(string='Reader Average rating', digits=(14, 4)) # Digits are optional
    cost_price = fields.Float(string='Book Cost', digits='Book Price')
    # let's add a currency fields
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary(string='Retail Price', currency_field='currency_id')  # currency_field is optionnal
    # relational fields
    publisher_id = fields.Many2one('res.partner', string='Publisher', ondelete='set null') # optionnal =>  context={}, domain=[]
    publisher_city = fields.Char(string='Publisher City', related='publisher_id.city', readonly=True)
    category_id = fields.Many2one('library.book.category', string='Categorie')

    # add an sql constrainst
    # _sql_constraints = [
    #     ('name_uniq', 'UNIQUE (name)',
    #         'Book title must be unique.'),
    #     ('positive_page', 'CHECK(pages>0)',
    #         'No of pages must be positive')
    # ]
    # contraint on release date
    # @api.constrains('date_release')
    # def _check_release_date(self):
    #     for record in self:
    #         if record.date_release and record.date_release > fields.Date.today():
    #             raise models.ValidationError('Release date must be in the past')

    # conputed fields
    age_days = fields.Float(string='Days Since Release', 
                compute='_compute_age',
                inverse='_inverse_age',
                search='_search_age',
                store=False,
                compute_sudo=True)

    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.date_release:
                delta = today - book.date_release
                book.age_days = delta.days
            else:
                book.age_days = 0

    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            book.date_release = today - timedelta(days=book.age_days)
    
    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        # convert the operator:
        # book with age > value have a date < value_date
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]

    #reference fields
    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([
            ('field_id.name','=','message_ids')])
        return [(x.model, x.name) for x in models]
    
    ref_doc_id = fields.Reference(selection='_referencable_models', string='Reference Document')
    


# inherit class for publisher
class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many('library.book', 'publisher_id', string='Published Books')
    authored_book_ids = fields.Many2many('library.book', string='Authored Books') # optionnal => relation='library_book_res_partner_rel' to shorten the relation fields
    count_books = fields.Integer(string='Number of Authored Books', compute='_compute_count_books')

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)


    