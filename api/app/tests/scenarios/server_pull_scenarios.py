test_cases = {
    "pull_all_communities_event": {
        "description": "Test server pull: 1 Event (All Communities)",
        "pull_technique": "full",
        "mock_event_search_response": [
            {
                "id": "1",
                "timestamp": "1655364474",
                "sighting_timestamp": "0",
                "published": True,
                "uuid": "572503da-c87f-4520-a9bc-8de08b9c92e5",
                "orgc_uuid": "10c8f445-888b-4a2d-bac8-4e1e8861d595",
            }
        ],
        "mock_event_view_response": {
            "Event": {
                "id": "1",
                "orgc_id": "1",
                "org_id": "1",
                "date": "2022-06-09",
                "threat_level_id": "1",
                "info": "test server pull (all communities)",
                "published": True,
                "uuid": "572503da-c87f-4520-a9bc-8de08b9c92e5",
                "attribute_count": "5",
                "analysis": "1",
                "timestamp": "1655364474",
                "distribution": "2",
                "proposal_email_lock": False,
                "locked": False,
                "publish_timestamp": "1655365142",
                "sharing_group_id": "0",
                "disable_correlation": False,
                "extends_uuid": "",
                "protected": None,
                "event_creator_email": "admin@admin.test",
                "Org": {
                    "id": "1",
                    "name": "HOST",
                    "uuid": "10c8f445-888b-4a2d-bac8-4e1e8861d595",
                    "local": True,
                },
                "Orgc": {
                    "id": "1",
                    "name": "HOST",
                    "uuid": "10c8f445-888b-4a2d-bac8-4e1e8861d595",
                    "local": True,
                },
                "Attribute": [
                    {
                        "id": "1",
                        "type": "ip-src",
                        "category": "Network activity",
                        "to_ids": False,
                        "uuid": "e437b43c-8b13-4599-9ccf-f31c61007dd2",
                        "event_id": "1",
                        "distribution": "5",
                        "timestamp": "1654760393",
                        "comment": "",
                        "sharing_group_id": "0",
                        "deleted": False,
                        "disable_correlation": False,
                        "object_id": "0",
                        "object_relation": None,
                        "first_seen": None,
                        "last_seen": None,
                        "value": "1.1.1.1",
                        "Galaxy": [],
                        "ShadowAttribute": [],
                        "Tag": [
                            {
                                "id": "4",
                                "name": "tlp:green",
                                "colour": "#00FF00",
                                "exportable": True,
                                "user_id": "0",
                                "hide_tag": False,
                                "numerical_value": None,
                                "is_galaxy": False,
                                "is_custom_galaxy": False,
                                "local_only": False,
                                "local": 0,
                            },
                        ],
                    }
                ],
                "ShadowAttribute": [],
                "RelatedEvent": [],
                "Galaxy": [],
                "Object": [
                    {
                        "id": "1",
                        "name": "ip-port",
                        "meta-category": "network",
                        "description": "An IP address (or domain or hostname) and a port seen as a tuple (or as a triple) in a specific time frame.",
                        "template_uuid": "9f8cea74-16fe-4968-a2b4-026676949ac6",
                        "template_version": "9",
                        "event_id": "1",
                        "uuid": "519090c8-470a-4429-9990-f771969cc375",
                        "timestamp": "1655213042",
                        "distribution": "5",
                        "sharing_group_id": "0",
                        "comment": "",
                        "deleted": False,
                        "first_seen": None,
                        "last_seen": None,
                        "ObjectReference": [
                            {
                                "id": "1",
                                "uuid": "ca7f0f25-80c8-4383-ae83-899ba96a36fc",
                                "timestamp": "1655454733",
                                "object_id": "1",
                                "referenced_uuid": "576a7264-0029-46e5-8eaa-771d3a9ec3d3",
                                "referenced_id": "2",
                                "referenced_type": "1",
                                "relationship_type": "uses",
                                "comment": "",
                                "deleted": False,
                                "event_id": "1",
                                "source_uuid": "519090c8-470a-4429-9990-f771969cc375",
                                "Object": {
                                    "distribution": "5",
                                    "sharing_group_id": "0",
                                    "uuid": "576a7264-0029-46e5-8eaa-771d3a9ec3d3",
                                    "name": "email",
                                    "meta-category": "network",
                                },
                            }
                        ],
                        "Attribute": [
                            {
                                "id": "3",
                                "type": "domain",
                                "category": "Network activity",
                                "to_ids": True,
                                "uuid": "201257fb-8d9e-4b27-ac26-d00cdf35a744",
                                "event_id": "1",
                                "distribution": "5",
                                "timestamp": "1655213042",
                                "comment": "",
                                "sharing_group_id": "0",
                                "deleted": False,
                                "disable_correlation": False,
                                "object_id": "1",
                                "object_relation": "domain",
                                "first_seen": None,
                                "last_seen": None,
                                "value": "evil.com",
                                "Galaxy": [],
                                "ShadowAttribute": [],
                                "Tag": [
                                    {
                                        "id": "1",
                                        "name": "tlp:red",
                                        "colour": "#FF0000",
                                        "exportable": True,
                                        "user_id": "0",
                                        "hide_tag": False,
                                        "numerical_value": None,
                                        "is_galaxy": False,
                                        "is_custom_galaxy": False,
                                        "local_only": False,
                                        "local": 0,
                                    },
                                ],
                            },
                            {
                                "id": "4",
                                "type": "port",
                                "category": "Network activity",
                                "to_ids": False,
                                "uuid": "75fa97cb-55ee-4bcf-af96-12c669c4283c",
                                "event_id": "1",
                                "distribution": "5",
                                "timestamp": "1655213042",
                                "comment": "",
                                "sharing_group_id": "0",
                                "deleted": False,
                                "disable_correlation": True,
                                "object_id": "1",
                                "object_relation": "dst-port",
                                "first_seen": None,
                                "last_seen": None,
                                "value": "54321",
                                "Galaxy": [],
                                "ShadowAttribute": [],
                            },
                            {
                                "id": "5",
                                "type": "ip-dst",
                                "category": "Network activity",
                                "to_ids": True,
                                "uuid": "0041ec54-a699-4984-8d6c-860cc9ef378b",
                                "event_id": "1",
                                "distribution": "5",
                                "timestamp": "1655213042",
                                "comment": "",
                                "sharing_group_id": "0",
                                "deleted": False,
                                "disable_correlation": False,
                                "object_id": "1",
                                "object_relation": "ip",
                                "first_seen": None,
                                "last_seen": None,
                                "value": "9.9.9.9",
                                "Galaxy": [],
                                "ShadowAttribute": [],
                            },
                        ],
                    },
                    {
                        "id": "2",
                        "name": "email",
                        "meta-category": "network",
                        "description": "Email object describing an email with meta-information",
                        "template_uuid": "a0c666e0-fc65-4be8-b48f-3423d788b552",
                        "template_version": "18",
                        "event_id": "1",
                        "uuid": "576a7264-0029-46e5-8eaa-771d3a9ec3d3",
                        "timestamp": "1655364474",
                        "distribution": "5",
                        "sharing_group_id": "0",
                        "comment": "",
                        "deleted": False,
                        "first_seen": None,
                        "last_seen": None,
                        "ObjectReference": [],
                        "Attribute": [
                            {
                                "id": "6",
                                "type": "email-src",
                                "category": "Payload delivery",
                                "to_ids": True,
                                "uuid": "f489ac2f-8f5e-4232-ac0d-f2e70839afdc",
                                "event_id": "1",
                                "distribution": "5",
                                "timestamp": "1655364474",
                                "comment": "",
                                "sharing_group_id": "0",
                                "deleted": False,
                                "disable_correlation": False,
                                "object_id": "2",
                                "object_relation": "from",
                                "first_seen": None,
                                "last_seen": None,
                                "value": "hacker@evil.com",
                                "Galaxy": [],
                                "ShadowAttribute": [],
                            }
                        ],
                    },
                ],
                "EventReport": [],
                "CryptographicKey": [],
                "Tag": [
                    {
                        "id": "1",
                        "name": "tlp:red",
                        "colour": "#FF0000",
                        "exportable": True,
                        "user_id": "0",
                        "hide_tag": False,
                        "numerical_value": None,
                        "is_galaxy": False,
                        "is_custom_galaxy": False,
                        "local_only": False,
                        "local": 0,
                    },
                ],
            }
        },
        "expected_result": {
            "event_uuids": (["572503da-c87f-4520-a9bc-8de08b9c92e5"]),
            "attribute_uuids": (
                [
                    "e437b43c-8b13-4599-9ccf-f31c61007dd2",
                    "201257fb-8d9e-4b27-ac26-d00cdf35a744",
                    "75fa97cb-55ee-4bcf-af96-12c669c4283c",
                    "0041ec54-a699-4984-8d6c-860cc9ef378b",
                    "f489ac2f-8f5e-4232-ac0d-f2e70839afdc",
                ]
            ),
            "object_uuids": (
                [
                    "519090c8-470a-4429-9990-f771969cc375",
                    "576a7264-0029-46e5-8eaa-771d3a9ec3d3",
                ]
            ),
            "object_reference_uuids": (["ca7f0f25-80c8-4383-ae83-899ba96a36fc"]),
            "sharing_groups_uuids": ([]),
            "sharing_group_org_uuids": ([]),
            "sharing_groups_servers_uuids": ([]),
            "tags": (["tlp:red", "tlp:green"]),
            "event_tags": (["tlp:red"]),
            "attribute_tags": (
                [
                    {
                        "attribute_uuid": "e437b43c-8b13-4599-9ccf-f31c61007dd2",
                        "tags": ["tlp:green"],
                    },
                    {
                        "attribute_uuid": "201257fb-8d9e-4b27-ac26-d00cdf35a744",
                        "tags": ["tlp:red"],
                    },
                ]
            ),
        },
    },
    "pull_sharing_group_event": {
        "description": "Test server pull: 1 Event (Sharing Group)",
        "pull_technique": "full",
        "mock_event_search_response": [
            {
                "id": "1",
                "timestamp": "1655364474",
                "sighting_timestamp": "0",
                "published": True,
                "uuid": "4e637837-da9c-4d3a-badd-5eb5b98ec324",
                "orgc_uuid": "9e93d085-17e0-4fb7-b790-300fbcf0af8a",
            }
        ],
        "mock_event_view_response": {
            "Event": {
                "id": "1",
                "orgc_id": "1",
                "org_id": "1",
                "date": "2022-06-09",
                "threat_level_id": "1",
                "info": "test server pull (sharing group)",
                "published": True,
                "uuid": "4e637837-da9c-4d3a-badd-5eb5b98ec324",
                "attribute_count": "1",
                "analysis": "1",
                "timestamp": "1655364474",
                "distribution": "4",
                "proposal_email_lock": False,
                "locked": False,
                "publish_timestamp": "1655365142",
                "sharing_group_id": "7",
                "disable_correlation": False,
                "extends_uuid": "",
                "protected": None,
                "event_creator_email": "admin@admin.test",
                "Org": {
                    "id": "1",
                    "name": "HOST",
                    "uuid": "9e93d085-17e0-4fb7-b790-300fbcf0af8a",
                    "local": True,
                },
                "Orgc": {
                    "id": "1",
                    "name": "HOST",
                    "uuid": "9e93d085-17e0-4fb7-b790-300fbcf0af8a",
                    "local": True,
                },
                "SharingGroup": {
                    "id": "7",
                    "name": "test sharing group",
                    "releasability": "",
                    "description": "",
                    "uuid": "81a93b6d-0f67-4696-abe0-42f5064610a3",
                    "organisation_uuid": "9e93d085-17e0-4fb7-b790-300fbcf0af8a",
                    "org_id": "1",
                    "sync_user_id": "0",
                    "active": True,
                    "created": "2022-07-01 10:15:57",
                    "modified": "2022-07-01 10:15:57",
                    "local": True,
                    "roaming": False,
                    "Organisation": {
                        "id": "1",
                        "name": "HOST",
                        "uuid": "9e93d085-17e0-4fb7-b790-300fbcf0af8a",
                    },
                    "SharingGroupOrg": [
                        {
                            "id": "11",
                            "sharing_group_id": "7",
                            "org_id": "1",
                            "extend": True,
                            "Organisation": {
                                "id": "1",
                                "name": "HOST",
                                "uuid": "9e93d085-17e0-4fb7-b790-300fbcf0af8a",
                            },
                        },
                        {
                            "id": "12",
                            "sharing_group_id": "7",
                            "org_id": "35",
                            "extend": False,
                            "Organisation": {
                                "id": "35",
                                "name": "ORG-A",
                                "uuid": "4862a5dd-c1cd-4488-967a-213f4214468d",
                            },
                        },
                        {
                            "id": "13",
                            "sharing_group_id": "7",
                            "org_id": "36",
                            "extend": False,
                            "Organisation": {
                                "id": "36",
                                "name": "ORG-B",
                                "uuid": "17814bd0-8976-492c-ab6c-4e121059a510",
                            },
                        },
                        {
                            "id": "14",
                            "sharing_group_id": "7",
                            "org_id": "26",
                            "extend": False,
                            "Organisation": {
                                "id": "26",
                                "name": "GUEST",
                                "uuid": "e2be8820-cac9-41c7-a190-6b57bbf2fc48",
                            },
                        },
                    ],
                    "SharingGroupServer": [
                        {
                            "id": "7",
                            "sharing_group_id": "7",
                            "server_id": "0",
                            "all_orgs": False,
                            "Server": {
                                "id": "0",
                                "url": "https://localhost",
                                "name": "https://localhost",
                            },
                        }
                    ],
                },
                "Attribute": [
                    {
                        "id": "1",
                        "type": "ip-src",
                        "category": "Network activity",
                        "to_ids": False,
                        "uuid": "70b688cf-e8d7-419a-9e0e-8fa85eeabbd2",
                        "event_id": "1",
                        "distribution": "5",
                        "timestamp": "1654760393",
                        "comment": "",
                        "sharing_group_id": "0",
                        "deleted": False,
                        "disable_correlation": False,
                        "object_id": "0",
                        "object_relation": None,
                        "first_seen": None,
                        "last_seen": None,
                        "value": "1.1.1.1",
                        "Galaxy": [],
                        "ShadowAttribute": [],
                        "Tag": [
                            {
                                "id": "4",
                                "name": "tlp:green",
                                "colour": "#00FF00",
                                "exportable": True,
                                "user_id": "0",
                                "hide_tag": False,
                                "numerical_value": None,
                                "is_galaxy": False,
                                "is_custom_galaxy": False,
                                "local_only": False,
                                "local": 0,
                            },
                        ],
                    }
                ],
                "ShadowAttribute": [],
                "RelatedEvent": [],
                "Galaxy": [],
                "Object": [],
                "EventReport": [],
                "CryptographicKey": [],
                "Tag": [
                    {
                        "id": "2",
                        "name": "tlp:amber",
                        "colour": "#FFC000",
                        "exportable": True,
                        "user_id": "0",
                        "hide_tag": False,
                        "numerical_value": None,
                        "is_galaxy": False,
                        "is_custom_galaxy": False,
                        "local_only": False,
                        "local": 0,
                    },
                ],
            }
        },
        "expected_result": {
            "event_uuids": (["4e637837-da9c-4d3a-badd-5eb5b98ec324"]),
            "attribute_uuids": (["70b688cf-e8d7-419a-9e0e-8fa85eeabbd2"]),
            "object_uuids": ([]),
            "object_reference_uuids": ([]),
            "sharing_groups_uuids": (["81a93b6d-0f67-4696-abe0-42f5064610a3"]),
            "sharing_group_org_uuids": (
                [
                    "9e93d085-17e0-4fb7-b790-300fbcf0af8a",
                    "4862a5dd-c1cd-4488-967a-213f4214468d",
                    "17814bd0-8976-492c-ab6c-4e121059a510",
                ]
            ),
            "sharing_groups_servers_uuids": (["81a93b6d-0f67-4696-abe0-42f5064610a3"]),
            "tags": (["tlp:amber", "tlp:green"]),
            "event_tags": (["tlp:amber"]),
            "attribute_tags": (
                [
                    {
                        "attribute_uuid": "70b688cf-e8d7-419a-9e0e-8fa85eeabbd2",
                        "tags": ["tlp:green"],
                    }
                ]
            ),
        },
    },
}
