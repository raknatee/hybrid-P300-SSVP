# ML-server API

## /db

### HTTP POST
- GUI needs to set those information to [Generial Collection]() for eeg-client and ML-server because they need to use it for collection naming.

### Request body

```json
{
    current_mode: "offline" | "online"
    current_participant_id: <str>
}
```

## /db

### HTTP GET

### Respone body

```json
{
    current_mode: "offline" | "online"
    current_participant_id: <str>
}
```

## /db/\<DATEBASE-NAME\>
### HTTP GET
- Return number of documents in each collection in particular Mongo database

Respone body
```json
{ 
    <Collectionname>: <int>
    ... 
    <Collectionname>: <int>
}
```


## /eeg_offline/\<PARTICIPANT-ID>
### WS
For EEG client submits a EEG signal package and save in the database.

This API needs to set PARTICIPANT-ID from [/db](#db)

### Flow
1. WS connection
2. client -> api (tells API about who you are)
```
SENDER|RECEIVER_LEN|RECEIVER_FULL
```
3. client -> api

```json
{
    "data": [

        {
            "timestamp": <timestamp(float of s)> ,
            "data": [ <float> , <float> , ..., <float> ]
            "second_counter": <int> 
        },

        {
            "timestamp": <timestamp(float of s)> ,
            "data": [ <float> , <float> , ..., <float> ]
            "second_counter": <int> 

        },

        ...

        {
            "timestamp": <timestamp(float of s)> ,
            "data": [ <float> , <float> , ..., <float> ]
            "second_counter": <int> 

        },

    ]

}
```
3. client <- api

```
1
```
4. repeat step 3

## /begin_offline_mode/\<PARTICIPANT-ID>
### WS
- A WS connection for begining the offline mode.

### Setup
1. Client knows what they need to do right? (how to run experiments)
2. target alphabets are decided by client side
3. Client needs to send timestamp of each round

### Flow
1. ws connection
2. client <- api (API needs to tell that I'm ready)
```json
{ "cmd": "next" }
```
3. client run the experiment
- Gap sleep for each round: **sleep 1000ms**
- highlight the target: **sleep 1000ms**
- back to rest/Zero state: **sleep 1000ms**
- run the experiment: **sleep 2000? ms**

4. client -> api (API saves the data to mongodb)
```json
{
    "target_grid": <int>,
    "target_index": <int>,
    "data":[
                {
                    "timestamp": <timestamp(float of s)>,
                    "is_target_activated": <bool>
                },
                {
                    "timestamp": <timestamp(float of s)>,
                    "is_target_activated": <bool>
                }
                ...  # noted: number == size of that grid
            ]
            

}
```
5. repect step 2

## /eeg_online/\<PARTICIPANT-ID>
### WS
Same as [/eeg_offline](#eeg-offline-participant-id) but for online mode.
Future Plan: add Timeout Index in Mongo


## /begin_online_mode/\<PARTICIPANT-ID>
### WS

### Setup
1. Client does not know anything. They just do the HYPS.
2. After did the round, Client just wait for API/Server to tell what grid and index should be.


### Flow
1. ws connection
2. client <- api (API needs to tell that I'm ready)
```json
{ "cmd": "next" }
```
3. client run the experiment
- Gap sleep for each round: **sleep 1000ms**
- run the experiment: **sleep 2000? ms**

4. client -> api (API saves the data to mongodb)
```json
{
    "begin_time": <timestamp(float of s)> ,
}
```
5. client <- api (model prediction)
- Gap for model prediction **sleep ?? ms**

```json
{
    "cmd": "output_model",
    "guessed_grid": <int> ,
    "guessed_index_order": <int>
}
```