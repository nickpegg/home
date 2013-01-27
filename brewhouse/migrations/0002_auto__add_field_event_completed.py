# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.completed'
        db.add_column('brewhouse_event', 'completed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.completed'
        db.delete_column('brewhouse_event', 'completed')


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
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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