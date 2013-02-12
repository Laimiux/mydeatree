var app = app || {}; ( function() {'use strict';

		// Idea Model
		// ----------
		app.Idea = Backbone.Model.extend({

			url : function() {
				return this.get('resource_uri') || this.collection.url();
			},
			methodUrl : {
				'create' : IDEA_API,

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
			sync : function(method, model, options) {
				if (model.methodUrl && model.methodUrl[method.toLowerCase()]) {
					options = options || {};
					options.url = model.methodUrl[method.toLowerCase()];
				}
				Backbone.sync(method, model, options);
			}
		});

	}());
