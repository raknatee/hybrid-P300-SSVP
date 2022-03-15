# Database model

- MongoDB is used
- Participant id must be UPPER CASE. Ex => A01S01 (First Participant of First Attempt)

## EEG-database
- database name

### \<PARTICIPANT-ID>-EEG-offline-collection
- Document Format (For each record)

```json
{
    _id: ObjectId(),
    timestamp: <timestamp(float of s)>
    data:[
        <float>,
        <float>,
        ...,
        <float>
    ],
}
```

### \<PARTICIPANT-ID>-experiment-offline-collection
- Document Format (For each record)
```json
{
    _id: ObjectId(),
    target_grid: <int>
    target_index: <int>
    data:[
            {
                timestamp: <timestamp(float of s)>
                is_target_activated: <bool>
            },
            ...,
            {
                timestamp: <timestamp(float of s)>
                is_target_activated: <bool>
            }
   
         ] 
}
```

### General-Collection
- Only one document object
```json
{
    _id: ObjectId(),
    type: "experiment_config",
    current_mode: "offline" | "online",
    current_participant_id: <string>, # Ex: A01S01, A01S02
    eeg_client_status: "connected" | "unconnected"
}
```

