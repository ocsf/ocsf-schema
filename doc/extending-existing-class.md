# How to Extend an Existing Class

## Overview

This document provides an example of how to extend the `Cloud` object, which is indirectly used in the `Base Event` class. The `Base Event` class has an `Event Origin` (`origin`) attribute, which has an instance of the `Cloud` object (`cloud`). The simplified `Base Event` class definition looks like:

```json
{
  "origin": {
    "cloud": {
      // The Cloud object's attributes
    }
    // Other origin's attributes
  }
  // Other base_event's attributes
}
```

## The Goal

The goal is to add an additional string attribute, `comment`, to the `Cloud` object and then "extend" the `Base Event` class to use the new `Cloud` object.

Note, for the purpose of this document, the existing `splunk_dev` schema extension will be used.

## New Cloud Object

Create a new object (`cloud_ex.json`) in the `extensions/splunk_dev/objects` folder:

```json
{
  "name": "Better Cloud",
  "type": "cloud_ex",
  "description": "The Better Cloud object describes a cloud with a comment.",
  "extends": "cloud",
  "attributes": {
    "comment": {
      "requirement": "recommended"
    }
  }
}
```

The new `Better Cloud` object extends the existing `Cloud` object and adds one *recommended* attribute, `comment`, to the existing `Cloud` object.

## New Event Origin Object

Create a new object (`origin_ex.json`) in the `extensions/splunk_dev/objects` folder:

```json
{
  "name": "Better Event Origin",
  "type": "event_origin_ex",
  "description": "The Better Event Origin with an added comment to the cloud object.",
  "extends": "event_origin",
  "attributes": {
    "cloud": {
      "object_type": "splunk_dev/cloud_ex"
    }
  }
}

```

The new `Better Event Origin` object extends the existing `Event Origin` object and overwrites the `object_type` of the `cloud` attribute as `"splunk_dev/cloud_ex"`.

## New Event Base Class 

If you are planning to use the new  `Better Cloud` object in many classes, then create a new "base event" class in the `extensions/splunk_dev/events` folder. For example,  `event_ex.json` file:

```json
{
  "name": "Better Event",
  "type": "event_ex",
  "extends": "base_event",
  "description": "A slightly better event using the better cloud.",
  "attributes": {
    "origin": {
      "object_type": "splunk_dev/event_origin_ex"
    }
  }
}
```

The new `Better Event` class extends the existing `Base Event` class and overwrites the `object_type` of the `origin` attribute as `"splunk_dev/event_origin_ex"`.

## Update Existing Class

If you are planning to use the new  `Better Cloud` object in a single class or just is a few classes, then you can overwrite the `object_type` of the `origin` attribute as `"splunk_dev/event_origin_ex"` directly in the class definition. For example:

```json
{
  "name": "Diagnostic Event",
  "type": "diagnostic",
  "category": "diagnostic",
  "uid": 1,
  "extends": "base_event",
  "attributes": {
    "activity_id": {
      "enum": {
        "1": {
          "name": "Logged"
        }
      }
    },
    "process": {
      "group": "primary",
      "requirement": "optional"
    },
    "origin": {
      "object_type": "splunk_dev/event_origin_ex"
    },
    "status_id": {
      "group": "primary",
      "requirement": "recommended"
    }    
  }
}

```

