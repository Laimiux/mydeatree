var app = app || {};

(function() {
	'use strict';
	
	// Idea Model
	// ----------
	app.Idea = Backbone.Model.extend({
		url : function() {
			return this.get('resource_uri') || this.collection.url;
		},
		
		toggleToParent: function() {
			app.AppView.toggleToParent(this.get('resource_uri'));
		}
	});
	
}());
