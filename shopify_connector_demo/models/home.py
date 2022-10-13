# -*- coding: utf-8 -*-
from odoo import fields,models


class Homedashbord(models.Model):
  """Home dashbord"""
  _name = "home.dashbord"
  _description = "Home Dashbord page"
 
 
  output = fields.Text(string="Output")
