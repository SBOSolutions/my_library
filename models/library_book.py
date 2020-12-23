# -*- coding: utf-8 -*-
from odoo import models, fields, api


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
    publisher_id = fields.Many2one('res.partner', string='Publisher', ondelete='set null') # it's optionnal =>  context={}, domain=[]
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


# inherit class for publisher
class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many('library.book', 'publisher_id', string='Published Books')
    authored_book_ids = fields.Many2many('library.book', string='Authored Books') # optionnal => relation='library_book_res_partner_rel' to shorten the relation fields


    