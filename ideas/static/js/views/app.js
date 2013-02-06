var app = app || {};

$(function($) {'use strict';

	app.AppView = Backbone.View.extend({
		el : $('#app'),

		events : {
			'click #createNewIdea' : 'createNewIdea',
			'scroll' : 'checkScroll',
		},

		initialize : function() {
			_.bindAll(this, 'addOne', 'showTopIdeas', 'addOneToTop', 'render', 'checkScroll');
			// bind to window a scroll fucntion
			$(window).scroll(this.checkScroll);

			//app.ideas = new IdeaList();
			//app.Ideas.bind('parent-change', this.addChildren, this);
			app.Ideas.on('reset', this.addAll);
			app.Ideas.on('add', this.addOneToTop)
			//app.Ideas.bind('add', this.addOneToTop);
			//app.Ideas.bind('refresh', this.addAll);
			app.Ideas.isLoading = true;
			app.Ideas.bind('all', this.render);
			app.Ideas.fetch({
				data : {
					order_by : '-modified_date'
				},
				update : true,
				remove : false,
				success : function() {
					app.Ideas.isLoading = false;
				}
			});

		},

		render : function() {
			if (app.ParentIdea && app.ParentIdea != '') {
				this.showChildrenIdeas(app.ParentIdea);
			} else {
				this.showTopIdeas();
			}
		},

		showChildrenIdeas : function(parent) {
			// Remove all old ideas from DOM
			this.$('#ideas').html('');

			// Get children ideas of a parent
			var childrenIdeas = app.Ideas.where({
				parent : IDEA_API + parent + "/"
			})
			console.log(childrenIdeas)
			_.each(childrenIdeas, this.addOne)
		},

		showTopIdeas : function() {
			// Remove all old ideas from DOM
			this.$('#ideas').html('');

			// Get ideas that don't have a parent
			var topIdeas = app.Ideas.where({
				parent : null
			});
			console.log(topIdeas);
			// Display those ideas
			_.each(topIdeas, this.addOne);
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

		checkScroll : function() {
			var triggerPoint = 100;
			// 100px from the bottom
			if (!app.Ideas.isLoading && !app.Ideas.completedSync && this.el.scrollTop + this.el.clientHeight + triggerPoint > this.el.scrollHeight) {
				// Load next page
				app.Ideas.isLoading = true;
				app.Ideas.fetch({
					update: true,
					remove: false,
					success: function(ideas) {
						app.Ideas.isLoading = false;		
					}
				});
			}
		}
	});

});
