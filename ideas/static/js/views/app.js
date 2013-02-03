var app = app || {};

$(function($) {'use strict';

	app.AppView = Backbone.View.extend({
		el : $('#app'),

		events : {
			'click #createNewIdea' : 'createNewIdea',
		},

		initialize : function() {
			_.bindAll(this, 'addOne', 'addAll', 'addOneToTop', 'render', 'toggleToParent');
			//app.ideas = new IdeaList();
			app.Ideas.bind('add', this.addOneToTop);
			app.Ideas.bind('refresh', this.addAll);
			app.Ideas.bind('all', this.render);
			app.Ideas.fetch({
				data : {
					order_by : '-modified_date'
				}
			});
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

		addOneToTop : function(idea) {
			var view = new app.IdeaView({
				model : idea
			})
			this.$('#ideas').prepend(view.render().el)
		},

		createNewIdea : function() {
			var title = this.$('#id_title').val();
			var text = this.$('#id_text').val();

			var hmm = app.Ideas.create({
				title : title,
				text : text
			}, {
				wait : true,
				success : function(model, response) {

					$('#newIdeaModal').modal('hide');
					$('#id_title').val('')
					$('#id_text').val('')
				},
				error : function(model, response) {
					var error = $.parseJSON(response.responseText);
					var idea = error.idea;

					var isTitleError = typeof idea.title != 'undefined';
					var isTextError = typeof idea.text != 'undefined';

					if (isTitleError || isTextError) {
						var error_field = $('#idea_error_field');
						error_field.empty()
						
						error_field.append("<h5>Errors:</h5><ul>");

						if (isTitleError) {
							error_field.append("<li>" + idea.title + "</li>");
						}
						if (isTextError) {
							error_field.append("<li>" + idea.text + "</li>");
						}

						error_field.append("</ul>");

					}
				}
			});

		},

		count : function() {
			return app.Ideas.length;
		},

		toggleToParent : function(parent_uri) {

		}
	});

});
