var app = app || {};
( function() {'use strict';

		// Idea Model
		// ----------
		app.Favorite = Backbone.Model.extend({

			urlRoot: function(){
   				 if (this.isNew()){
      				return "/api/v1/favorite_items/";
    			} else {
      				return "/api/v1/favorite_items/" + this.pk;
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

		});

	}());