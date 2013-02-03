var app = app || {}; ( function() {'use strict';

		// Idea Model
		// ----------
		app.Idea = Backbone.Model.extend({
			url : function() {
				return this.get('resource_uri') || this.collection.url;
			},

			validate : function(attrs) {
				this.errors = [];
				if (attrs.errors && attrs.errors.length > 0) {
					for (var key in attrs.errors) {
						this.errors.push(attrs.errors[key].errorMessage);
					}
				}
				return _.any(this.errors) ? this.errors : null;
			},

			toggleToParent : function() {
				app.AppView.toggleToParent(this.get('resource_uri'));
			}
		});

	}());
