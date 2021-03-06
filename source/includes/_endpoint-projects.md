## Projects

Projects represent groups of users or teams that share a common set of datasets. Any user
can belong to none or many projects.

They live under /projects/ and will list the projects that the authenticated user
is a member or owner of.

### Catalog

The projects catalog will list all the projects the authenticated user is a member of.
Here you can create new projects via POST

#### GET

```http
GET /projects/ HTTP/1.1
```

```json
{
  "element": "shoji:catalog",
  "self": "http://app.crunch.io/api/projects/",
  "index": {
    "http://app.crunch.io/api/projects/4643/": {
      "name": "Project 1",
      "id": "4643",
      "icon": "",
      "permissions": {"view":true, "edit": "true"}
    },
    "http://app.crunch.io/api/projects/6c01/": {
      "name": "Project 2",
      "id": "6c01",
      "icon": "",
      "description": "Description of project 2",
      "permissions": {"view":true, "edit": "true"}
    }
  }
}
```

Name | Type | Default | Description
-----|------|---------|-------------
name | string | | Required when creating the project
description | string | "" | Longer description pf tje [rpkect
id | string | autogenerated | The project's id
icon | url | "" | Url for the icon file for the project. Empty string if not set
permissions | object | {} | permissions possessed by querying user against project

#### POST

New projects need a name (no uniqueness enforced) and will make the authenticated
user its initial member and editor.

```http
POST /projects/ HTTP/1.1
```

Payload example:

```json
{
    "body": {
        "name": "My new project",
        "icon_url": "http://cdn.sample.com/project-icon.png"
    }
}
```

##### Creating a project with an icon

To create one with a starting icon you can POST an `icon_url` attribute 
indicating a url where to fetch that icon from (has to be a publicly accessible url).

If the server cannot read that URL the request will return a 409 error.

On success a copy of the file will be stored as the icon to be serve

If the `icon_url` attribute is not provided the API will pick an available icon 
from the icons catalog.

#### Default icon

The API can provide default icons to be used in new projects. Performing a GET
request will return a Shoji:catalog with a list of available icons for the client
to pick.
 
 
```http
GET /icons/ HTTP/1.1
```

```json
{
  "element": "shoji:catalog",
  "self": "http://app.crunch.io/api/icons/",
  "index": {
    "http://app.crunch.io/api/icons/01/": {},
    "http://app.crunch.io/api/icons/02/": {},
    "http://app.crunch.io/api/icons/03/": {},
    "http://app.crunch.io/api/icons/04/": {}
  }
}
```


### Entity

#### GET

```http
GET /projects/6c01/ HTTP/1.1
```

```json
{
  "element": "shoji:entity",
  "self": "http://app.crunch.io/api/projects/6c01/",
  "catalogs": {
    "datasets": "http://app.crunch.io/api/projects/6c01/datasets/",
    "members": "http://app.crunch.io/api/projects/6c01/members/"
  },
  "views": {
    "icon": "http://app.crunch.io/api/projects/6c01/icon/"
  },
  "body": {
    "name": "Project 2",
    "description": "Long description text",
    "icon": "",
    "user_icon": false,
    "id": ""
  }
}
```

Name | Type | Default | Description
-----|------|---------|-------------
name | string | | Required when creating the project
description | string | "" | Longer description of the project
id | string | autogenerated | The project's id
icon | url | "" | Url for the icon file for the project; empty string if not set
user_icon | boolean | autogenerated | Will indicate false if the icon used on creation is from the provided catalog

Note about the `icon` attribute that points to the actual image file where the
configured icon is. This url does not point to the `views.icon` Shoji view url.

The `views.icon` Shoji view endpoint is used to PUT the icon as a file upload
for this project.

#### PATCH

The attributes that are allowed to be edited for a projet are: 

 * name
 * description
 * icon_url
 
Only project editors can make these changes.

#### DELETE

Deleting a project will *NOT* delete its datasets. It will change their 
ownership to the authenticated user. Only the project current owner can delete 
a project.

```http
DELETE /projects/6c01/ HTTP/1.1
```

### Projects order

Returns the `shoji:order` in which the projects should be displayed for
 the user. This entity is independent for each user.
 
As the user is added to more projects, these will be added at the end of the
`shoji:order`.
 
#### GET

Will return a `shoji:order` containing a flat list of all the projects where
the current user belongs to.


```http
GET /projects/order/ HTTP/1.1
```

```json
{
  "element": "shoji:order",
  "self": "http://app.crunch.io/api/projects/order/",
  "graph": [
    "https://app.crunch.io/api/projects/cc9161/",
    "https://app.crunch.io/api/projects/a598c7/"
  ]
}
```

#### PUT

In order to change the order of the projects, the client will need to PUT the
full payload back to the server.

The graph attribute should contain all projects included, else it will return
a 400 response.

After a successful PUT request, the server will reply with a 204 response.

```http
PUT /projects/order/ HTTP/1.1
```

```json
{
  "element": "shoji:order",
  "self": "http://app.crunch.io/api/projects/order/",
  "graph": [
    "https://app.crunch.io/api/projects/cc9161/",
    "https://app.crunch.io/api/projects/a598c7/"
  ]
}
```

### Members

Use this endpoint to manage the users that have access to this project.

#### Members permissions

Members of a project can be either viewers or editors. By default all members
will be viewers and a selected group of them (at least one) will be editor.

These permissions are available on the members catalog under the `permissions` 
attribute on each member's tuple.

The possible permissions are:

 * edit
 * view
 
That can have boolean values. Those with `edit: true` are considered project 
editors.

Project editors have edit privileges on all datasets as well as permissions to
make changes on the project itself such as changing its name, icon, members 
management or change members' permissions.

A project can have users or teams as members. Teams represent groups of users
to be handled together. When a team gets access to a project, all members of
the team inherit those permissions. In the case that a user has access
to a project through several teams or direct access, the final permissions
will be added together.

#### GET

Returns a catalog with all users and teams that have access to this project and 
their project permissions in the following format:

```http
GET /projects/abcd/members/ HTTP/1.1
```

```json
{
  "element": "shoji:catalog",
  "self": "http://app.crunch.io/api/projects/6c01/members/",
  "index": {
    "http://app.crunch.io/api/users/00002/": {
      "name": "Jean-Luc Picard",
      "email": "captain@crunch.io",
      "collaborator": false,
      "permissions": {
        "edit": true,
        "view": true
      },
      "allowed_dataset_permissions": {
        "edit": true,
        "view": true
      }
    },
    "http://app.crunch.io/api/users/00005/": {
      "name": "William Riker",
      "email": "firstofficer@crunch.io",
      "collaborator": false,
      "permissions": {
        "edit": false,
        "view": true
      },
      "allowed_dataset_permissions": {
        "edit": false,
        "view": true
      }
    },
    "http://app.crunch.io/api/teams/000a5/": {
      "name": "Viewers teams",
      "permissions": {
        "edit": false,
        "view": true
      }
    }
  }
}
```

The catalog will be indexed by each entity's URL and its tuple will contain
basic information (name and email) as well as the permissions each user has
on the given project.

All project members have read access to this resource, but the 
`allowed_dataset_permissions` is only present to project editors. It contains
the maximum dataset permissions each user can have. Assigning anything more
permissive will not have effect.

#### PATCH

Use this method to add or remove members from the project. Only project editors 
have this capabilities, else you will get a 403 response.

To add a new user, PATCH a catalog keyed by the new user URL and an empty
object for its value or a permissions tuple to set specific permissions 
(only `edit` allowed at this point).

To remove users, PATCH a catalog keyed by the user you want to remove and `null`
for its value.

Note that you cannot remove yourself from the project, you will
get a 400 response.

It is possible to perform many additions/removals in one request, the 
following example adds users `/users/001/` and deletes users `/users/002/`

It is allowed to invite/add users to the project by email address. If the email
is registered on the system the user will be invited to the project. If the email
is not part of Crunch.io a new user invitation will be sent to that email with
instructions to set up their account. They will be automatically part of this
project only.

Attempting to remove users also allows to do so by email. In the case that the
email does not exist, the server will return a 400 response.


```http
PATCH /projects/abcd/members/ HTTP/1.1
```

```json
{
  "element": "shoji:catalog",
  "self": "http://app.crunch.io/api/projects/6c01/members/",
  "index": {
    "http://app.crunch.io/api/users/001/": {},
    "http://app.crunch.io/api/teams/00a/": {},
    "http://app.crunch.io/api/users/002/": {
      "permissions": {
        "edit": true
      }
    },
    "http://app.crunch.io/api/users/003/": null,
    "user@email.com": {},
    "send_notification": true,
    "url_base": "https://app.crunch.io/password/change/${token}/",
    "project_url": "https://app.crunch.io/${project_id}/",
  }
}
```

##### Sending notifications

The users invited to a project can be both existing Crunch.io users or new
users that don't have a user account associated with the email.

If desired, the API can send automated email notifications to the involved users
indicating that they now belong to the project.

It is necessary to add the `send_notification` boolean key on the index PATCHed
to command the API to send these emails. Else, no notification will be sent.

When sending notifications, it is necessary for the client to include a 
`url_base` key as well that includes a string template that should point to a
client location where the password resetting should happen for brand new users.

The server will replace the `${token}` part of the string with the generated
token and will be included on the notification email as a link for the invited 
user to configure their account in order to use the app.

Additionally, to indicate the URL of the project, the client can provide a
`project_url` key that should be formatted as a URL containing a `${project_id}`
part that the server will replace with the project's ID.

This behavior is the same as described for [inviting new users when sharing a dataset](#inviting-new-users)


### Users

A read only endpoint that lists all the individual users that have access to
this project, independent from their access type (via team or direct project 
membership).

The payload shares a similar shape as the members endpoint, but this catalog
contains only users.


```http
GET /projects/abcd/users/ HTTP/1.1
```

```json
{
  "element": "shoji:catalog",
  "self": "http://app.crunch.io/api/projects/6c01/members/",
  "index": {
    "http://app.crunch.io/api/users/00002/": {
      "name": "Jean-Luc Picard",
      "email": "captain@crunch.io",
      "collaborator": false,
      "allowed_dataset_permissions": {
        "edit": true,
        "view": true
      },
      "teams": []
    },
    "http://app.crunch.io/api/users/00005/": {
      "name": "William Riker",
      "email": "firstofficer@crunch.io",
      "collaborator": false,
      "allowed_dataset_permissions": {
        "edit": false,
        "view": true
      },
      "teams": ["http://app.crunch.io/api/teams/000a5/"]
    }
  }
}
```



### Datasets

Will list all the datasets that have this project as their owner.

#### Adding datasets to projects

The way to add a dataset to a project is by changing the dataset's owner to the
id of the project you want to take ownership.

You must have edit and be current editor on any given dataset to change its
owner and you must also have edit permissions on the target project.

#### PATCH to dataset entity

Send a PATCH request to the dataset entity that you want to make part of the
project.

```http
PATCH /datasets/cc9161/ HTTP/1.1
```

```json
{"owner":"https://app.crunch.io/api/projects/abcd/"}
```

#### GET

Will show the list of all datasets where this project is their owner, the 
shape of the dataset tuple will be the same as in other dataset catalogs.


```http
GET /projects/6c01/datasets/ HTTP/1.1
```

```json
{
  "element": "shoji:catalog",
  "self": "http://app.crunch.io/api/projects/6c01/datasets/",
  "orders": {
    "order": "http://app.crunch.io/api/projects/6c01/datasets/order/"
  },
  "index": {
    "https://app.crunch.io/api/datasets/cc9161/": {
        "owner_name": "James T. Kirk",
        "name": "The Voyage Home",
        "description": "Stardate 8390",
        "archived": false,
        "permissions": {
            "edit": false,
            "change_permissions": false,
            "view": true
        },
        "size": {
            "rows": 1234,
            "columns": 67
        },
        "id": "cc9161",
        "owner_id": "https://app.crunch.io/api/users/685722/",
        "start_date": "2286",
        "end_date": null,
        "streaming": "no",
        "creation_time": "1986-11-26T12:05:00",
        "modification_time": "1986-11-26T12:05:00",
        "current_editor": "https://app.crunch.io/api/users/ff9443/",
        "current_editor_name": "Leonard Nimoy"
    },
    "https://app.crunch.io/api/datasets/a598c7/": {
        "owner_name": "Spock",
        "name": "The Wrath of Khan",
        "description": "",
        "archived": false,
        "permissions": {
            "edit": true,
            "change_permissions": true,
            "view": true
        },
        "size": {
            "rows": null,
            "columns": null
        },
        "id": "a598c7",
        "owner_id": "https://app.crunch.io/api/users/af432c/",
        "start_date": "2285-10-03",
        "end_date": "2285-10-20",
        "streaming": "no",
        "creation_time": "1982-06-04T09:16:23.231045",
        "modification_time": "1982-06-04T09:16:23.231045",
        "current_editor": null,
        "current_editor_name": null
    }
  }
}
```

### Icon

The icon endpoint for a project is a ShojiView that allows to change the
project's icon via file upload or URL.

#### GET

On GET, it will return a `shoji:view` with its value containing a url to the
icon file or empty string in case there isn't an icon for this project yet.

By default all new projects have an empty icon URL.


```http
GET /projects/6c01/icon/ HTTP/1.1
```


```json
{
  "element": "shoji:view",
  "self": "http://app.crunch.io/api/projects/6c01/icon/",
  "value": ""
}
```

#### PUT

PUT to this endpoint to change a project's icon.

There are two ways to change the icon, either via file upload or via icon URL.

Only the project's editors can change the project's icon.
 
Valid image extensions: 'png', 'gif', 'jpg', 'jpeg' - Others will 400

##### File upload

The request should have be a standard `multipart/form-data` file upload with
 the file field named `icon`.
The file's contents will be stored and made available under the project's url.
The API will return a 201 response with the stored icon's URL on its Location 
header.


```http
PUT /projects/6c01/icon/ HTTP/1.1
Content-Disposition: form-data; name="icon"; filename="newicon.jpg"
Content-Type: image/jpeg
```

```http
HTTP/1.1 201 Created
Location: https://app.crunch.io/api/datasets/223fd4/
```

##### Icon URL

Expects a `Shoji:view` request with its value pointing to a publicly accessible
image resource that will be used as the project's icon. This image will be
copied to an API local location.

```http
PUT /projects/6c01/datasets/icon/ HTTP/1.1
```

```json
{
  "element": "shoji:view",
  "self": "http://app.crunch.io/api/projects/6c01/datasets/icon/",
  "value": "http://public.domain.com/icon.png"
}
```


```http
HTTP/1.1 201 Created
Location: https://app.crunch.io/api/datasets/223fd4/
```

#### POST

Same as PUT


### Datasets order

Contains the `shoji:order` in which the datasets of this project are to be 
ordered.

This is endpoint available for all project members but can only be updated by 
the project's editors.

#### GET

Will return the `shoji:order` response containing the datasets that belong
to the project.

```http
GET /projects/6c01/datasets/order/ HTTP/1.1
```

```json
{
  "element": "shoji:order",
  "self": "http://app.crunch.io/api/projects/6c01/datasets/order/",
  "graph": [
    "https://app.crunch.io/api/datasets/cc9161/",
    "https://app.crunch.io/api/datasets/a598c7/"
  ]
}
```

#### PUT

Allow to make modifications to the `shoji:order` for the contained datasets.
Only the project's editors can make these changes.

Trying to include an invalid dataset or an incomplete list will return a 
400 response.

```http
PUT /projects/6c01/datasets/order/ HTTP/1.1
```

```json
{
  "element": "shoji:order",
  "self": "http://app.crunch.io/api/projects/6c01/datasets/order/",
  "graph": [
    "https://app.crunch.io/api/datasets/cc9161/",
    {
      "group": "https://app.crunch.io/api/datasets/a598c7/"
    }
  ]
}
```

