# yahoo_mall_crawler

A crawler for gathering all buyers' comments per shop from Yahoo Mall


## Environment
    python 3.6.0

## How to execute?

    $python3 comment_crawler.py [seller_id]
    
## Example
    $python3 comment_crawler.py watsons
    
## Ouput format
JSON file

	{
	    "seller_name": ...,
	    "corporation": ...,
	    "representative": ...,
	    "tel": ...,
	    "fax": ...,
	    "address": ...,
	    "start_date": ...,
	    "seller_id": ...,
	    "comments":[
		{
		    "buyer_id": buyer's id,
		    "score": score from buyer,
		    "content": content of buyer's comment,
		    "date": when buyer left the comment
		},
		{
		    ...
		},
		...
	    ]
	}
