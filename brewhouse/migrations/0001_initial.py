# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Beer'
        db.create_table('brewhouse_beer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('recipe_url', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal('brewhouse', ['Beer'])

        # Adding model 'Event'
        db.create_table('brewhouse_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brewhouse.Beer'])),
            ('fermenter', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['brewhouse.Fermenter'], null=True, blank=True)),
            ('event_type', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('brewhouse', ['Event'])

        # Adding unique constraint on 'Event', fields ['beer', 'event_type']
        db.create_unique('brewhouse_event', ['beer_id', 'event_type'])

        # Adding model 'Tap'
        db.create_table('brewhouse_tap', (
            ('number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('beer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brewhouse.Beer'], null=True, blank=True)),
        ))
        db.send_create_signal('brewhouse', ['Tap'])

        # Adding model 'Fermenter'
        db.create_table('brewhouse_fermenter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('brewhouse', ['Fermenter'])


    def backwards(self, orm):
        # Removing unique constraint on 'Event', fields ['beer', 'event_type']
        db.delete_unique('brewhouse_event', ['beer_id', 'event_type'])

        # Deleting model 'Beer'
        db.delete_table('brewhouse_beer')

        # Deleting model 'Event'
        db.delete_table('brewhouse_event')

        # Deleting model 'Tap'
        db.delete_table('brewhouse_tap')

        # Deleting model 'Fermenter'
        db.delete_table('brewhouse_fermenter')


    models = {
        'brewhouse.beer': {
            'Meta': {'object_name': 'Beer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'recipe_url': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'brewhouse.event': {
            'Meta': {'ordering': "['-beer', '-date', '-id']", 'unique_together': "(('beer', 'event_type'),)", 'object_name': 'Event'},
            'beer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brewhouse.Beer']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'event_type': ('django.db.models.fields.IntegerField', [], {}),
            'fermenter': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['brewhouse.Fermenter']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'brewhouse.fermenter': {
            'Meta': {'object_name': 'Fermenter'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'brewhouse.tap': {
            'Meta': {'object_name': 'Tap'},
            'beer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brewhouse.Beer']", 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['brewhouse']