var app = app || {};

$(function($) {
	'use strict';
	
	app.AppView = Backbone.View.extend({
		el : $('#app'),

		events : {
			'click .idea' : 'createIdea',
		},

		initialize : function() {
			_.bindAll(this, 'addOne', 'addAll','addOneToTop', 'render', 'toggleToParent');
			//app.ideas = new IdeaList();
			app.Ideas.bind('add', this.addOneToTop);
			app.Ideas.bind('refresh', this.addAll);
			app.Ideas.bind('all', this.render);
			app.Ideas.fetch({data: {order_by: '-modified_date'}});
		},

		render : function() {
			this.addAll();
		},

		addAll : function() {
			app.Ideas.each(this.addOne);
		},

		addOne : function(idea) {
			var view = new app.IdeaView({
				model : idea
			});
			this.$('#ideas').append(view.render().el);
		},
		
		addOneToTop: function(idea) {
			var view = new app.IdeaView({
				model : idea
			})	
			this.$('#ideas').prepend(view.render().el)
		},

		createIdea : function() {
			var title = this.$('#title').val();
			var text = this.$('#text').val();
			if (title && text) {
				app.Ideas.create({
					title : title,
					text : text
				});

				this.$('#title').val('')
				this.$('#text').val('')
			}
		},
		
		
		count : function() {
			return app.Ideas.length;
		},
		
		toggleToParent: function(parent_uri) {
			
		}
	});

	
});
