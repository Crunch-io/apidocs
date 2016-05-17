## Datasets
Datasets are the primary containers of statistical data in Crunch. Datasets
contain a collection of [variables](#variables), with which analyses can be
composed, saved, and exported. These analyses may include filters, which users
can define and persist. Users can also share datasets with each other.

Datasets are comprised of one or more batches of data uploaded to Crunch, and
additional batches can be appended to datasets. Similarly, variables from other
datasets can be joined onto a dataset.

As with other objects in Crunch, references to the set of dataset entities are
exposed in a catalog. This catalog can be organized and ordered.

### Catalog

#### GET
```http
GET /datasets/ HTTP/1.1
```
```shell
```
```r
library(crunch)
login()

# Upon logging in, a GET /datasets/ is done automatically, to populate:
listDatasets() # Shows the names of all datasets you have
listDatasets(refresh=TRUE) # Refreshes that list (and does GET /datasets/)

# To get the raw Shoji object, should you need it,
crGET("https://beta.crunch.io/api/datasets/")
```

```python
```

```json
{
    "element": "shoji:catalog",
    "self": "https://beta.crunch.io/api/datasets/",
    "orders": {
        "order": "https://beta.crunch.io/api/datasets/order/"
    },
    "index": {
        "https://beta.crunch.io/api/datasets/cc9161/": {
            "owner_name": "James T. Kirk",
            "name": "The Voyage Home",
            "description": "Stardate 8390",
            "archived": false,
            "permissions": {
                "edit": false,
                "change_permissions":,
                "add_users":,
                "change_weight":,
                "view": true
            },
            "size": {
                "rows": 1234,
                "columns": 67
            },
            "id": "cc9161",
            "owner_id": "https://beta.crunch.io/api/users/685722/",
            "start_date": "2286",
            "end_date": null,
            "creation_time": "1986-11-26T12:05:00",
            "modification_time": "1986-11-26T12:05:00",
            "current_editor": "https://beta.crunch.io/api/users/ff9443/",
            "current_editor_name": "Leonard Nimoy"
        },
        "https://beta.crunch.io/api/datasets/a598c7/": {
            "owner_name": "Spock",
            "name": "The Wrath of Khan",
            "description": "",
            "archived": false,
            "permissions": {
                "edit": true,
                "change_permissions":,
                "add_users":,
                "change_weight":,
                "view": true
            },
            "size": {
                "rows": null,
                "columns": null
            },
            "id": "a598c7",
            "owner_id": "https://beta.crunch.io/api/users/af432c/",
            "start_date": "2285-10-03",
            "end_date": "2285-10-20",
            "creation_time": "1982-06-04T09:16:23.231045",
            "modification_time": "1982-06-04T09:16:23.231045",
            "current_editor": null,
            "current_editor_name": null
        }
    }
}
```

`GET /datasets/`

When authenticated, GET returns 200 status with a Shoji Catalog of datasets to
which the authenticated user has access. Catalog tuples contain the following
attributes:

Name | Type | Default | Description
---- | ---- | ------- | -----------
name | string |  | Required. The name of the dataset
description | string | "" | A longer description of the dataset
id | string |  | The dataset's id
archived | bool | false | Whether the dataset is "archived" or active
permissions | object | `{"edit": false}` | Authorizations on this dataset. See [Permissions](#permissions).
owner_id | URL |  | URL of the user entity of the dataset's owner
owner_name | string | "" | That user's name, for display
size | object | `{"rows": null, "columns": null}` | Dimensions of the dataset
creation_time | ISO-8601 string |  | Datetime at which the dataset was created in Crunch
modification_time | ISO-8601 string | | Datetime of the last modification for this dataset globally
start_date | ISO-8601 string |  | Date/time for which the data in the dataset corresponds
end_date | ISO-8601 string |  | End date/time of the dataset's data, defining a start_date:end_date range
current_editor | URL or null | | URL of the user entity that is currently editing the dataset, or `null` if there is no current editor
current_editor_name | string or null | | That user's name, for display

<aside class="notice">
    A user may have access to a dataset because someone has shared it directly
    with him, or because someone has shared it with a team of which he is a
    member. If a user has access to a dataset from different sources, be it by
    multiple teams or by direct sharing, the final permissions they have on the
    dataset will be the maximum of all the permissions granted.
</aside>

#### PATCH
```http
PATCH /api/datasets/ HTTP/1.1
Host: beta.crunch.io
Content-Type: application/json
Content-Length: 231

{
    "element": "shoji:catalog",
    "index": {
        "https://beta.crunch.io/api/datasets/a598c7/": {
            "description": "Stardate 8130.4"
        }
    }
}

```

```http
HTTP/1.1 204 No Content
```
```r
library(crunch)
login()

# Dataset objects contain information from
# the catalog tuple and the dataset entity.
# Editing attributes by <- assignment will
# PATCH or PUT the right payload to the
# right place--you don't have to think about
# catalogs and entities.
ds <- loadDataset("The Wrath of Khan")
description(ds)
## [1] ""
description(ds) <- "Stardate 8130.4"
description(ds)
## [1] "Stardate 8130.4"

# If you needed to touch HTTP more directly,
# you could:
payload <- list(
    `https://beta.crunch.io/api/datasets/a598c7/`=list(
        description="Stardate 8130.4"
    )
)
crPATCH("https://beta.crunch.io/api/datasets/",
    body=toJSON(payload))
```
```shell
```
```python
```

`PATCH /datasets/`

Use PATCH to edit the "name", "description", "start_date", "end_date", or
"archived" state of one or more datasets. A successful request returns a 204
response. The attributes changed will be seen by all users with access to this
dataset; i.e., names, descriptions, and archived state are not merely attributes
 of your view of the data but of the datasets themselves.

Authorization is required: you must have "edit" privileges on the dataset(s)
being modified, as shown in the "permissions" object in the catalog tuples. If
you try to PATCH and are not authorized, you will receive a 403 response and no
changes will be made.

The tuple attributes other than "name", "description", and "archived" cannot be
modified here by PATCH. Attempting to modify other attributes, or including new
attributes, will return a 400 response. Changing permissions is accomplished by
PATCH on the permissions catalog, and changing the owner is a PATCH on the
dataset entity. The "owner_name" and "current_editor_name" attributes are
modifiable, assuming authorization, by PATCH on the associated user entity.
Dataset "size" is a cached property of the data, changing only if the number of
rows or columns in the dataset change. Dataset "id", "modification_time"
and "creation_time" are immutable/system generated.

When PATCHing, you may include only the keys in each tuple that are being
modified, or you may send the complete tuple. As long as the keys that cannot
be modified via PATCH here are not modified, the request will succeed.

Note that, unlike other Shoji Catalog resources, you cannot PATCH to add new
datasets, nor can you PATCH a null tuple to delete them. Attempting either will
return a 400 response. Creating datasets is allowed only by POST to the catalog,
 while deleting datasets is accomplished via a DELETE on the dataset entity.

##### Changing ownership

Any changes to the ownership of a dataset need to be done by the current editor.

Only the dataset owner can change the ownership to another user. This can be done
by PATCH request with the new owners' email of API URL. The new owner must have
advanced permissions on Crunch.

Other editors of the dataset can change the ownership of a dataset only to a
Project as long as they andthe current owner of the dataset are both editors
on such project.



#### POST
```http
POST /api/datasets/ HTTP/1.1
Host: beta.crunch.io
Content-Type: application/json
Content-Length: 88

{
    "element": "shoji:entity",
    "body": {
        "name": "Trouble with Tribbles",
        "description": "Stardate 4523.3"
    }
}

```

```http
HTTP/1.1 201 Created
Location: https://beta.crunch.io/api/datasets/223fd4/

```
```r
library(crunch)
login()

# To create just the dataset entity, you can
ds <- createDataset("Trouble with Tribbles",
    description="Stardate 4523.3")

# More likely, you'll have a data.frame or
# similar object in R, and you'll want to send
# it to Crunch. To do that,
df <- read.csv("~/tribbles.csv")
ds <- newDataset(df, name="Trouble with Tribbles",
    description="Stardate 4523.3")
```
```shell
```
```python
```

`POST /datasets/`

POST a JSON object to create a new Dataset; a 201 indicates success, and the
returned Location header refers to the new Dataset resource.

The body must contain a "name", and additional parameters "description" and
"archived" are allowed. You can also include a Crunch Table in a "table" key,
as discussed in the Feature Guide. Sending any other attribute will return a 400 response.

### Other catalogs

In addition to `/datasets/`, there are a few other catalogs of datasets in the API:

#### Team datasets

`/teams/{team_id}/datasets/`

A Shoji Catalog of datasets that have been shared with this team. These datasets
are not included in the primary dataset catalog. See [teams](#teams) for more.

#### Filter datasets by name

`/datasets/by_name/{dataset_name}/`

The `by_name` catalog returns (on GET) a Shoji Catalog that is a subset of
`/datasets/` where the dataset name matches the "dataset_name" value. Matches
are case sensitive.

Verbs other than GET are not supported on this subcatalog. PATCH and POST at
 the primary dataset catalog.

### Dataset order

The dataset order allows each user to organize the order in which their datasets
are presented.

This endpoint returns a `shoji:order`. Like all shoji orders, it may not contain
all available datasets. The catalog should always be the authoritative source
of available datasets.

Any dataset not present on the order graph should be considered to be at the
bottom of the root list in arbitrary order.

#### GET

`GET /datasets/{dataset_id}/order/`

```json

{
    "element": "shoji:order",
    "self": "/datasets/{dataset_id}/order/",
     "graph": [
        "dataset_url",
        {"group": [
            "dataset_url"        
        ]}
     ]
}
```

#### PUT

Receives a complete `shoji:order` payload and replaces the existing graph
with the new one.

It cannot contain dataset references that are not in the dataset catalog, else
the API will return a 400 response.

Standard `shoji:order` graph validation will apply.

#### PATCH

Same semantics as PUT



### Entity

#### GET

`GET /datasets/{dataset_id}/`

##### URL Parameters

Parameter | Description
--------- | -----------
dataset_id | The id of the dataset

##### Dataset attributes

Name | Type | Default | Description
---- | ---- | ------- | -----------
name | string |  | Required. The name of the dataset
description | string | "" | A longer description of the dataset
notes | string | "" | Additional information you want to associate with this dataset
id | string |  | The dataset's id
archived | bool | false | Whether the dataset is "archived" or active
permissions | object | `{"edit": false}` | Authorizations on this dataset. See [Permissions](#permissions).
owner_id | URL |  | URL of the user entity of the dataset's owner
owner_name | string | "" | That user's name, for display
size | object | `{"rows": null, "columns": null}` | Dimensions of the dataset
creation_time | ISO-8601 string |  | Datetime at which the dataset was created in Crunch
start_date | ISO-8601 string |  | Date/time for which the data in the dataset corresponds
end_date | ISO-8601 string |  | End date/time of the dataset's data, defining a start_date:end_date range
current_editor | URL or null | | URL of the user entity that is currently editing the dataset, or `null` if there is no current editor
current_editor_name | string or null | | That user's name, for display
weight | URL | null | Points to the current weight variable applied for the given user

#### PATCH

`PATCH /datasets/{dataset_id}/`

See above about PATCHing the dataset catalog for all attributes duplicated on
the entity and the catalog. You may PATCH those attributes on the entity, but you
are encouraged to PATCH the catalog instead. The two attributes appearing on the
entity and not the catalog, "notes" and "weight", are modifiable by PATCH here.

A successful PATCH request returns a 204 response. The attributes changed will be seen
by all users with access to this dataset; i.e., names, descriptions, and archived
state are not merely attributes of your view of the data but of the datasets themselves.

Authorization is required: you must have "edit" privileges on this dataset.
 If you try to PATCH and are not authorized, you will receive a 403 response
 and no changes will be made. If you have edit permissions but are not the
 current editor of this dataset, PATCH requests of anything other than
 "current_editor" will respond with 409 status. You will need first to PATCH to
 make yourself
  the current editor and then proceed to make the desired changes.

When PATCHing, you may include only the keys that are being
modified, or you may send the complete entity. As long as the keys that cannot be
modified via PATCH here are not modified, the request will succeed.

##### Changing dataset ownership

If you are the current editor of a dataset you can change its owner by PATCHing
the `owner` attribute witht he URL of the new owner.

Only Users, Teams or Projects can be set as owners of a dataset.

* Users: New owner needs to be advanced users to be owner of a dataset.
* Teams: Authenticated user needs to be a member of the team.
* Projects: Authenticated user needs to have edit permissions on the project.


#### DELETE

`DELETE /datasets/{dataset_id}/`

With sufficient authorization, a successful DELETE request removes the dataset
from the Crunch system and responds with 204 status.

#### Views

##### Applied filters

##### Cube

`/datasets/{id}/cube/?q`

See [Multidimensional Analysis](#multidimensional-analysis).

##### Export

`/datasets/{id}/export/`

GET returns a Shoji View of available dataset export formats.

```json
{
	"element": "shoji:view",
	"self": "https://beta.crunch.io/api/datasets/223fd4/export/",
	"views": {
		"spss": "https://beta.crunch.io/api/datasets/223fd4/export/spss/",
		"csv": "https://beta.crunch.io/api/datasets/223fd4/export/csv/"
	}
}
```

Accessing any of the export URLs will return a `shoji:view` with an attribute
`url` pointing to the location of the exported file to be downloaded.

Following rules apply for all formats:

* All exporting happens synchronously.
* If the dataset does not have any columns, the server will return a 409 response
* Hidden/discarded variables are not exported.
* Onnly exclusion filter will be applied.
* User applied filters are not applied.
* Personal(private) variables are not exported.


###### SPSS

Will contain all non personal variables in the same flat order as organized.
Derived variables will be exported as normal variables and arrays as supported
by SPSS.

###### CSV

Will only export base non personal variables in the same flat order as organized
in the API.

Categorical variables will be exported with their name instead of their value.



##### Summary

`/datasets/{id}/summary/{?filter}`

###### Query Parameters

Parameter | Description
--------- | -----------
filter | A Crunch filter expression

GET returns a Shoji View with summary information about this dataset containing
 its number of rows (weighted and unweighted, with and without your applied
 filters), as well as the number of variables and columns. The column count
 will differ from the variable count when derived and array variables are
 present--these variable types don't necessarily have their own columns of d
 ata behind them. The column count is useful for estimating load time and
 file size when exporting.

If a `filter` is included, the "filtered" counts will be with respect to that
expression. If omitted, your applied filters will be used.

```json
{
	"element": "shoji:view",
	"self": "https://beta.crunch.io/api/datasets/223fd4/summary/",
	"value": {
		"unweighted": {
			"filtered": 2000,
			"total": 2000
		},
        "weighted": {
            "filtered": 2000.0,
            "total": 2000.0
        },
		"variables": 529,
		"columns": 530
	}
}
```


#### Fragments

##### Table

##### State

##### Exclusion

`/datasets/{id}/exclusion/`

Exclusion filters allow you to drop rows of data without permanently deleting them.

GET on this resource returns a Shoji Entity with a filter "expression" attribute
in its body. Rows that match the filter expression will be excluded from all views of the data.

PATCH the "expression" attribute to modify. An empty "expression" object, like
 `{"body": {"expression": {}}}`, is equivalent to "no exclusion", i.e. no rows
 are dropped.

##### Stream

##### Decks

`/datasets/{id}/decks/`

Decks allow you to store [saved analyses](#saving-analyses) as slides on them
for exporting or future reference.

Decks are personal per dataset and each dataset gets one by default but it is
possible to create more as necessary by POSTing to the decks catalog. They
only need a name.

###### GET

A GET request on the catalog endpoint will return all the decks available for
this dataset for the authenticated user.

```json
{
    "element": "shoji:catalog",
    "self": "https://beta.crunch.io/api/datasets/223fd4/decks/",
    "index": {
        "https://beta.crunch.io/api/datasets/cc9161/decks/4fa25/": {
          "name": "my new deck",
          "creation_time": "1986-11-26T12:05:00",
        },
        "https://beta.crunch.io/api/datasets/cc9161/decks/2b53e/": {
          "name": "Default deck",
          "creation_time": "1987-10-15T11:45:00",
        },
    },
    "order": "https://beta.crunch.io/api/datasets/223fd4/decks/order/"
}

```

###### POST

POST will create a new decks for this dataset. It only needs to have
identifiable name.

```json
{
    "element": "shoji:entity",
    "self": "https://beta.crunch.io/api/datasets/223fd4/decks/",
    "body": {
        "name": "my new deck"
    }
}
```

```http
HTTP/1.1 201 Created
Location: https://beta.crunch.io/api/datasets/223fd4/decks/2b3c5e/

```

###### Deck entity

`/datasets/{id}/decks/{id}/`

####### GET

You can GET on the deck entity to see all its attributes:

```json
{
    "element": "shoji:entity",
    "self": "https://beta.crunch.io/api/datasets/223fd4/decks/223fd4/",
    "body": {
        "name": "Presentation deck",
        "id": "223fd4",
        "creation_time": "1987-10-15T11:45:00",
        "description": "Explanation about the deck"
    }
}
```

####### PATCH

In order to change the name or description of a deck you can PATCH a shoji:entity to it. The server will return a 204 response.

```json
{
    "element": "shoji:entity",
    "self": "https://beta.crunch.io/api/datasets/223fd4/decks/223fd4/",
    "body": {
        "name": "Presentation deck",
        "id": "223fd4",
        "creation_time": "1987-10-15T11:45:00",
        "description": "Explanation about the deck"
    }
}
```
```http
HTTP/1.1 204 No Content
```


###### Decks order

`/datasets/{id}/decks/order/`

The Deck order allows to the user to customize the order in which they will be
displayed by an API client.

The deck order will always contain all existing decks.

####### GET

Will return a (Shoji Order)[#shoji-order] payload.

```json
{
  "element": "shoji:order",
  "self": "https://beta.crunch.io/api/datasets/223fd4/decks/order/",
  "graph": [
    "https://beta.crunch.io/api/datasets/223fd4/decks/1/",
    "https://beta.crunch.io/api/datasets/223fd4/decks/2/",
    "https://beta.crunch.io/api/datasets/223fd4/decks/3/"
  ]
}

```

####### PATCH

It is necessary to do a PATCH request to change the order of the decks. On success the server will return a 204 response.

If the payload contains only a subset of the existing decks. The unmentioned decks will be always appended at the bottom of the top level graph in arbitrary order.

```json
{
  "element": "shoji:order",
  "self": "https://beta.crunch.io/api/datasets/223fd4/decks/order/",
  "graph": [
    "https://beta.crunch.io/api/datasets/223fd4/decks/1/",
    "https://beta.crunch.io/api/datasets/223fd4/decks/3/"
  ]
}
```

Including invalid URLs or URLs to decks that are not present in the catalog will return a 400 response from the server.


##### Preferences

`/datasets/{id}/preferences/`

The dataset preferences provide API clients with a key/value store for settings
or customizations each would need for each user.

By default all dataset preferences start out as an empty object where clients can
PATCH the keys each deems necessary.

```json
{
    "element": "shoji:entity",
    "self": "https://beta.crunch.io/api/datasets/223fd4/preferences/",
    "body": {}
}
```

To delete keys from the preferences the value needs to be patched with `null`.

There is no order associated with the saved preferences. Clients should assume
they are in arbitrary order.


#### Catalogs

##### Batches

##### Filters

##### Variables

##### Actions

##### Savepoints

##### Weight variables

##### Joins

##### Multitables

##### Comparisons

##### Forks

##### Permissions
