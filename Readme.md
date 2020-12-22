# Bridgewell-bidding server
This is a bidding server demo porject, including SQL database, DSP-server, and SSP-client.

## SQL databsae
Constrcut advertising setting with MySQL, the spec. & testing data are show below:

### `ad_setting` Schema

| Column name  | Type |               Comment              |
|--------------|------|------------------------------------|
| creative_id  | int  | The id of advertising creative     |
| status       | bool | Bidding switch                     |
| bidding_cpm  | int  | Cost per 1000 impression           |


### testing data

| creative_id | status | bidding_cpm |
|-------------|--------|-------------|
|      1      |  true  |       5     |
|      2      |  false |       5     |
|      3      |  true  |       7     |
|      4      |  true  |       2     |
|      5      |  true  |       9     |

## DSP-server
### DSP-server will execute following things: </br> 
1. Accept http post from SSP-client.
2. Load testing data from local database, and start bidding process.
3. Send response to SSP-client with highest bidding price & id, the response body is shown below

```json
{
   "price": 15.00,
   "creative_id": 1,
}
```

## SSP-client
### SSP-client will execute following things: </br>
1. Post request to DSP-server, the post body is shown below:
```json
{
"bid_floor": 12.00
}
```
2. Accept response from DSP-server.

## How to use
1. Load ad_settings to MySQL, and modify ```db_settings``` in SQL_database.py
2. Execute DSP_Server.py
3. Execute SSP_Client.py
