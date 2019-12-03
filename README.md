# rawsocket-distance

## Usage:
Please include a `targets.txt` file in the same folder as the script.
`python distMeasurement.py`
The script will rewrite `results.csv` or create the file if it does not exist.

## Execution Notes:
tmall.com, nih.gov, businessinsider.com, medicalnewstoday.com, superuser.com, and oschina.net did not respond.

On a run on 12/2/19, rambler.ru did not respond. This is okay, since I have 11 total sites. The final submission contains rambler.ru

I am using youtube.com, onlinevideoconverter.com, 1337x.to, znds.com, wildberries.ru, crunchyroll.com, and indiamart.com to replace them

## Conclusions
On analysis of the data, 2 distinct trends were visible.
First, most .com, .com.ua, and .to sites except znds.com and onlinevideoconverter.com responded almost instantly, while anything else (.ru) took significantly longer to respond.

Running the tool against sites in quick succession led to an increased likelihood of the traceroute-style packet being dropped. This occurred specifically for rambler.ru

Anything over 12 hops took significantly longer than anything less. This is probably due to a transoceanic hop occurring between hops 13 and 15.

I graphed RTT logarithmically to better visualize relations. Two groups were immediately distinct. As far as I can tell, the large difference in RTTs for hop counts over 15 and below 13 is apparent.


### Here's some data.

The average time for per hop 1.53ms RTT.
The standard deviation for all data was 1.72 ms.
This won't do, let's split the data into 2 groups, high RTT/hop and low RTT/hop (these match nicely to <13 and >15 hops)

The high group average RTT per hop was 3.34ms
The high group's standard deviation was 0.86ms

The low group's average RTT per hop was 0.037ms, which seems very low.
The standard deviation for the low group was 0.011ms.

### Notes
I realized soon before the deadline that I didn't correctly calculate RTT. It is too late to fix, but I would just extract the RTT from both the packet header and the ICMP error information and sum them. To correct, I assumed that RTT was the same for both outgoing and incoming messages.
