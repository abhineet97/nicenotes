(function ($, Backbone, _, app) {
  var TemplateView = Backbone.View.extend({
    templateName: '',
    initialize: function () {
      this.template = _.template($(this.templateName).html());
    },
    render: function () {
      var context = this.getContext(),
        html = this.template(context);
      this.$el.html(html);
    },
    getContext: function () {
      return {};
    }
  });

  var FormView = TemplateView.extend({
    events: {
      'submit form': 'submit'
    },
    errorTemplate: _.template('<span class="pure-form-message error"><%- msg %></span>'),
    clearErrors: function () {
      $('.error', this.form).remove();
    },
    showDialog: function () {
      this.render();
      var dialog = this.$el.dialog({
        autoOpen: false, 
        modal: true,
        width: 500,
        classes: {
          "ui-dialog": "ui-corner-all",
          "ui-dialog-titlebar": "ui-corner-all custom-ui-dialog-titlebar",
          "ui-dialog-titlebar-close": "no-close",
        }
      });
      dialog.dialog('open');
    },
    showErrors: function (errors) {
      _.map(errors, function(fieldErrors, name) {
        var field = $(':input[name' + name + ']', this.form),
          label = $('label[for=' + field.attr('id') + ']', this.form);
        if (label.length === 0) {
          label = $('label', this.form).first();
        }
        function appendError(msg) {
          label.before(this.errorTemplate({msg: msg}));
        }
        _.map(fieldErrors, appendError, this);
      }, this);
    },
    modelFailure: function (model, xhr, options) {
      var errors = xhr.responseJSON;
      this.showErrors(errors);
    },
    serializeForm: function (form) {
      return _.object(_.map(form.serializeArray(), function (item) {
        return [item.name, item.value];
      }));
    },
    submit: function (e) {
      e.preventDefault();
      this.form = $(e.currentTarget);
      this.clearErrors();
    },
    failure: function (xhr, status, error) {
      var errors = xhr.responseJSON;
      this.showErrors(errors);
    },
    done: function (e) {
      if (e) {
        e.preventDefault();
      }
      this.trigger('done');
      this.remove();
    }
  });

  var LoginView = FormView.extend({
    id: 'login',
    templateName: '#login-template',
    submit: function (event) {
      var data = {};
      FormView.prototype.submit.apply(this, arguments);
      data = this.serializeForm(this.form);
      $.post(app.apiLogin, data)
        .done($.proxy(this.loginSuccess, this))
        .fail($.proxy(this.failure, this));
    },
    loginSuccess: function (data) {
      app.session.save(data.token);
      this.done();
    }
  });
  app.views.LoginView = LoginView;

  var RegisterView = FormView.extend({
    id: 'register',
    templateName: '#register-template',
    submit: function (event) {
      var data = {};
      FormView.prototype.submit.apply(this, arguments);
      data = this.serializeForm(this.form);
      $.post(app.api.users, data)
        .done($.proxy(this.registerSuccess, this))
        .fail($.proxy(this.failure, this));
    },
    registerSuccess: function (data) {
      app.session.save(data.token);
      this.done();
    }
  });
  app.views.RegisterView = RegisterView;

  var NotesView = TemplateView.extend({
    events: {
      'click button.delete-note': 'removeNote',
      'click button.edit-note': 'editNote',
      'click button.share-note': 'shareNote',
      'click button#new-note': 'createNote'
    },
    templateName: '#notes-template',
    initialize: function (options) {
      var self = this;
      TemplateView.prototype.initialize.apply(this, arguments);
      app.notes.fetch({
        success: $.proxy(self.render, self)
      });
    },
    removeNote: function (event) {
      var self = this;
      id = $(event.currentTarget).parent().attr('data-id');
      event.preventDefault();
      note = app.notes.get(id);
      note.destroy({
        success: function(model, res) {
          self.render();
        },
        failure: function () {alert('Failed to delete note');}
      });
    },
    createNote: function(event) {
      var self = this;
      var view = new CreateNoteView();
      event.preventDefault();
      this.$el.after(view.el);
      view.showDialog();
      view.on('done', function () { self.render(); });
    },
    editNote: function (event) {
      var self = this;
      $parentEl = $(event.currentTarget).parent();
      id = $parentEl.attr('data-id');
      note = app.notes.get(id);
      view = new EditNoteView({model: note});
      event.preventDefault();
      this.$el.after(view.el);
      view.showDialog();
      view.on('done', function () { self.render(); });
    },
    shareNote: function (event) {
      var self = this;
      id = $(event.currentTarget).parent().attr('data-id');
      note = app.notes.get(id);
      view = new ShareNoteView({model: note});
      event.preventDefault();
      this.$el.after(view.el);
    },
    getContext: function () {
      return {notes: app.notes || null, title: 'Your Notes', sharedView: false};
    }
  });
  app.views.NotesView = NotesView;

  var CreateNoteView = FormView.extend({
    tagName: 'div',
    attributes: {
      'title': 'Add a New Note'
    },
    events: _.extend({
      'reset': 'done'
    }, FormView.prototype.events),
    templateName: '#create-note-template',
    submit: function (event) {
      var self = this,
        attributes = {};
      FormView.prototype.submit.apply(this, arguments);
      attributes = this.serializeForm(this.form);
      app.notes.create(attributes, {
        wait: true,
        success: $.proxy(self.success, this),
        error: $.proxy(self.modelFailure, this)
      });
    },
    success: function (model) {
      this.done();
    }
  });
  app.views.CreateNoteView = CreateNoteView;

  var EditNoteView = FormView.extend({
    tagName: 'div',
    attributes: {
      'title': 'Edit Note'
    },
    events: _.extend({
      'reset': 'done'
    }, FormView.prototype.events),
    templateName: '#edit-note-template',
    submit: function (event) {
      var self = this,
        attributes = {};
      FormView.prototype.submit.apply(this, arguments);
      attributes = this.serializeForm(this.form);
      self.model.save(attributes, {
        wait: true,
        success: $.proxy(self.success, this),
        error: $.proxy(self.modelFailure, this)
      });
    },
    success: function (model) {
      this.done();
    },
    getContext: function () {
      return {note: this.model};
    }
  });
  app.views.EditNoteView = EditNoteView;

  var UserListView = FormView.extend({
    tagName: 'ul',
    className: 'user-list',
    userList: null,
    templateName: '#user-list-template',
    getContext: function () {
      return {users: this.userList};
    }
  });
  app.views.UserListView = UserListView;

  var ShareNoteView = FormView.extend({
    tagName: 'div',
    attributes: {
      'title': 'Share Note'
    },
    events: _.extend({
      'reset': 'done',
      'change #id_access': 'changeAccess',
      'input #search': 'filterUserList'
    }, FormView.prototype.events),
    templateName: '#share-note-template',
    listView: null,
    initialize: function (options) {
      var self = this;
      FormView.prototype.initialize.apply(this, arguments);
      app.users.fetch({
        success: $.proxy(this.listUsers, self)
      });
    },
    changeAccess: function(event) {
      var self = this,
        userid = $(event.currentTarget).parent().attr('data-user-id');
      var attributes = {
        view_access_to: self.model.get('view_access_to'),
        edit_access_to: self.model.get('edit_access_to')
      };
      var access = $(event.currentTarget).val();
      attributes.view_access_to = _.without(attributes.view_access_to, Number(userid));
      attributes.edit_access_to = _.without(attributes.edit_access_to, Number(userid));
      if (access !== 'none') {
        attributes[access + '_access_to'].push(userid);
      }
      self.model.save(attributes, {
        wait: true,
        success: $.proxy(self.success, self),
        fail: $.proxy(self.modelFailure, self)
      });
    },
    filterUserList: function (event) {
      query = $(event.currentTarget).val();
      this.listView.userList = app.users.filter(function(user){
        return user.get('mobile').toLowerCase().includes(query) ||
          user.get('full_name').toLowerCase().includes(query);
      });
      this.listView.render();
    },
    listUsers: function (collection, res, options) {
      _.each(collection.models, function (model) {
        if(this.model.get('edit_access_to').includes(model.get('id'))) {
          model.set({access: 'edit'});
        } else if (this.model.get('view_access_to').includes(model.get('id'))) {
          model.set({access: 'view'});
        } else {
          model.set({access: 'none'});
        }
      }, this);
      this.listView = new UserListView();
      this.listView.userList = collection.models;
      this.showDialog();
      this.$el.children('form').append(this.listView.el);
      this.listView.render();
    },
    submit: function (event) {
      var self = this,
        attributes = {};
      FormView.prototype.submit.apply(this, arguments);
      self.model.save(attributes, {
        wait: true,
        success: $.proxy(self.success, self),
        error: $.proxy(self.modelFailure, self)
      });
    },
    success: function (model) {
      this.done();
    },
    getContext: function () {
    }
  });
  app.views.ShareNoteView = ShareNoteView;

  var SharedView = TemplateView.extend({
    templateName: '#notes-template',
    initialize: function (options) {
      var self = this;
      TemplateView.prototype.initialize.apply(this, arguments);
      app.me.fetch({
        success: $.proxy(this.addNote, self)
      });
    },
    addNote: function (collections, response, options) {
      app.notes.reset();
      _.each(response.edit_access_to, function(note) {
        note.access = 'edit';
        app.notes.push(note);
      });
      _.each(response.view_access_to, function(note) {
        note.access = 'view';
        app.notes.push(note);
      });
      this.render();
    },
    getContext: function () {
      return {notes: app.notes || null, title: 'Shared Notes', sharedView: true};
    }
  });
  app.views.SharedView = SharedView;

  var HeaderView = TemplateView.extend({
    tagName: 'header',
    templateName: '#header-template',
    events: {
      'click a#logout': 'logout',
    },
    getContext: function() {
      return {authenticated: app.session.authenticated()};
    },
    logout: function(e) {
      e.preventDefault();
      app.session.delete();
      window.location = '/';
    }
  });
  app.views.HeaderView = HeaderView;


})(jQuery, Backbone, _, app);
