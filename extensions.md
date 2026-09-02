# OCSF Extensions Registry

The purpose of this file is to keep track of and avoid collisions in Extension `names` and `uid`s.

`Repository` is optional. Use it when the extension schema is public (in the [OCSF GitHub org](https://github.com/ocsf) or elsewhere). Leave it blank for private extensions or when the code is not published.

| Caption     | Name     | UID | Notes | Repository |
|-------------|----------|-----|-------|------------|
| DefenXee    | defenxee | **987** | The DefenXee vendor extension| | 
| Trellix     | trellix  | **988** | The Trellix schema extension | |
| Synqly      | synqly   | **989** | The Synqly schema extension | |
| US GOV      | usg1     | **990** | The USG-1 schema extension | |
| Cisco       | cisco    | **991** | The Cisco schema extension | |
| Sedara      | sedara   | **992** | The Sedara schema extension | |
| Sciber      | sciber   | **993** | The Sciber schema extension | |
| DataBee     | databee  | **994** | The Comcast DataBee schema extension | |
| Symantec    | symantec | **995** | The Symantec schema extension | [ocsf/symantec](https://github.com/ocsf/symantec) |
| SentinelOne | s1       | **996** | The SentinelOne schema extension | |
| Splunk      | splunk   | **997** | The Splunk schema extension | [ocsf/splunk](https://github.com/ocsf/splunk) |
| AWS         | aws      | **998** | The Amazon Web Services schema extension | [ocsf/aws](https://github.com/ocsf/aws) |
| Development | dev      | **999** | The development (TODO) schema extensions | [ocsf/dev-ext](https://github.com/ocsf/dev-ext) |
| _Native Extensions defined in OCSF_ |
| Linux       | linux    | **1** | The Linux extension defines Linux specific attributes, objects and classes | [extensions/linux](extensions/linux/) |
| Windows     | win      | **2** | The Windows extension defines Windows specific attributes, objects and classes | [extensions/windows](extensions/windows/) |
| macOS       | macos    | **3** | The macOS extension defines macOS specific attributes, profiles, objects and classes | [extensions/macos](extensions/macos/) |
