# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import (
    HiddenField, SubmitField, BooleanField,
    StringField, PasswordField, SelectField,
    TextAreaField, RadioField,
)
from wtforms.fields.html5 import (
    DateField, TimeField,
    URLField, EmailField,
)
from wtforms.validators import AnyOf, DataRequired, length

from datetime import time, datetime

from dribdat.user.models import User, Project, Event, Resource, Role
from ..user.validators import UniqueValidator
from ..user import (
    USER_ROLE, USER_STATUS,
    projectProgressList,
    resourceTypeList,
)

class UserForm(FlaskForm):
    next = HiddenField()
    id = HiddenField('id')
    username = StringField(u'Username', [length(max=80), UniqueValidator(User, 'username'), DataRequired()])
    email = EmailField(u'E-mail address', [length(max=80), DataRequired()])
    password = PasswordField(u'New password (optional)', [length(max=128)])
    is_admin = BooleanField(u"Administrator", default=False)
    active = BooleanField(u"Active", default=True)
    submit = SubmitField(u'Save')

class EventForm(FlaskForm):
    next = HiddenField()
    id = HiddenField('id')
    name = StringField(u'Title', [length(max=80), UniqueValidator(Event, 'name'), DataRequired()])
    starts_date = DateField(u'Starts date', default=datetime.now())
    starts_time = TimeField(u'Starts time', default=time(9,0,0))
    ends_date = DateField(u'Finish date', default=datetime.now())
    ends_time = TimeField(u'Finish time', default=time(16,0,0))
    hostname = StringField(u'Hosted by', [length(max=80)])
    location = StringField(u'Located at', [length(max=255)])
    description = TextAreaField(u'Description', description=u'Markdown and HTML supported')
    resources = TextAreaField(u'Information for participants, event page', description=u'Markdown and HTML supported')
    logo_url = URLField(u'Host logo link', [length(max=255)])
    webpage_url = URLField(u'Home page link', [length(max=255)])
    community_url = URLField(u'Community link', [length(max=255)])
    certificate_path = URLField(u'Participant certificate link', [length(max=1024)], description='Include {username}, {email} or {sso} identifier')
    boilerplate = TextAreaField(u'Getting started guide', description=u'Top of new project page, markdown and HTML supported')
    community_embed = TextAreaField(u'Code of conduct and community links', description=u'Bottom of event and project page, markdown, HTML and embedded scripts supported')
    custom_css = TextAreaField(u'Custom stylesheet', description=u'External CSS support: @import url(https://...);')
    is_current = BooleanField(u'Featured event shown on homepage (max 1)', default=False)
    is_hidden = BooleanField(u'Hide this event from the homepage', default=False)
    # copy_template = BooleanField(u'Copy template pitch into new projects', default=False)
    lock_editing = BooleanField(u'Block editing projects (Freeze)', default=False)
    lock_starting = BooleanField(u'Block starting new projects (Lock)', default=False)
    lock_resources = BooleanField(u'Block suggesting resources (Stun)', default=False)
    submit = SubmitField(u'Save')

class ProjectForm(FlaskForm):
    next = HiddenField()
    id = HiddenField('id')
    user_id = SelectField(u'Owner (team user)', coerce=int)
    event_id = SelectField(u'Event', coerce=int)
    category_id = SelectField(u'Challenge category', coerce=int)
    progress = SelectField(u'Progress', coerce=int, choices=projectProgressList())
    hashtag = StringField(u'Hashtag or channel', [length(max=255)])
    autotext_url = URLField(u'Sync', [length(max=255)])
    # is_autoupdate = BooleanField(u'Autoupdate project data')
    name = StringField(u'Title', [length(max=80), UniqueValidator(Project, 'name'), DataRequired()])
    summary = StringField(u'Short summary', [length(max=120)])
    longtext = TextAreaField(u'Description')
    autotext = TextAreaField(u'Readme content')
    webpage_url = URLField(u'Presentation or demo link', [length(max=2048)])
    is_webembed = BooleanField(u'Embed contents of demo link in a frame', default=False)
    source_url = URLField(u'Source link', [length(max=255)])
    contact_url = URLField(u'Contact link', [length(max=255)])
    image_url = URLField(u'Image link', [length(max=255)])
    logo_color = StringField(u'Custom color', [length(max=7)])
    logo_icon = StringField(u'Custom icon', [length(max=20)])
    # is_template = BooleanField(u'This project is used as a template for the event', default=False)
    submit = SubmitField(u'Save')

class CategoryForm(FlaskForm):
    next = HiddenField()
    name = StringField(u'Name', [length(max=80), DataRequired()])
    description = TextAreaField(u'Description', description=u'Markdown and HTML supported')
    logo_color = StringField(u'Custom color', [length(max=7)])
    logo_icon = StringField(u'Custom icon (fontawesome.io/icons)', [length(max=20)])
    event_id = SelectField(u'Specific to an event, or global if blank', coerce=int)
    submit = SubmitField(u'Save')

class ResourceForm(FlaskForm):
    next = HiddenField()
    id = HiddenField('id')
    name = StringField(u'Name', [length(max=80), UniqueValidator(Resource, 'name'), DataRequired()])
    user_id = SelectField(u'Owner', coerce=int)
    type_id = RadioField(u'Type', coerce=int, choices=resourceTypeList())
    source_url = URLField(u'Link', [length(max=2048)], description=u'URL to download or get more information')
    summary = TextAreaField(u'Summary', [length(max=140)], description=u'How is this useful: in 140 characters or less?')
    content = TextAreaField(u'Additional information', description=u'Describe this resource in detail, Markdown and HTML supported')
    progress_tip = SelectField(u'Recommend at', coerce=int, choices=projectProgressList(True, True), description=u'Progress level at which this resource should be suggested to teams')
    is_visible = BooleanField(u'Show this resource to participants', description='Enable DRIBDAT_TOOL_APPROVE to moderate all submissions')
    submit = SubmitField(u'Save')

class RoleForm(FlaskForm):
    next = HiddenField()
    id = HiddenField('id')
    name = StringField(u'Name', [length(max=80), UniqueValidator(Role, 'name'), DataRequired()])
    submit = SubmitField(u'Save')
