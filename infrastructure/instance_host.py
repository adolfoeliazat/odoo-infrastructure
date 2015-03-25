# -*- coding: utf-8 -*-
from openerp import models, fields, api


class instance_host(models.Model):

    """"""

    _name = 'infrastructure.instance_host'
    _description = 'instance_host'

    server_hostname_id = fields.Many2one(
        'infrastructure.server_hostname',
        string='Server Hostname',
        required=True
        )
    subdomain = fields.Char(
        string='Subdomain'
        )
    instance_id = fields.Many2one(
        'infrastructure.instance',
        string='instance_id',
        ondelete='cascade',
        required=True
        )
    name = fields.Char(
        'Name',
        required=True
        )
    server_id = fields.Many2one(
        'infrastructure.server',
        string='Server',
        related='instance_id.environment_id.server_id',
        store=True,
        readonly=True
        )
    type = fields.Selection(
        [('main', 'Main'),
         ('redirect_to_main', 'Redirect To Main'),
         ('other', 'Other')],
        string='Main?',
        default='main',
        )
    wildcard = fields.Boolean(
        string='Wildcard',
        related='server_hostname_id.wildcard'
        )

    _sql_constraints = [
        ('name_uniq', 'unique(name, server_id)',
            'Name must be unique per server!'),
    ]

    @api.onchange('server_hostname_id', 'subdomain', 'database_type_id')
    def _get_name(self):
        if self.server_hostname_id.wildcard:
            if self.subdomain:
                name = self.subdomain + '.' + self.server_hostname_id.name
            else:
                name = '*' + '.' + self.server_hostname_id.name
        else:
            name = self.server_hostname_id.name
        if self.database_type_id.url_prefix:
            name = self.database_type_id.url_prefix + '.' + name
        self.name = name
