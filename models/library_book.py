# -*- coding: utf-8 -*-
from odoo import models, fields


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
