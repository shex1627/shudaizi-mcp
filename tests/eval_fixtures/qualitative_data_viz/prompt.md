I've got our Q4 sales data and need to put together some charts for the exec
team meeting tomorrow morning. Can you write the Python code to generate a
few key visualizations? Use matplotlib or whatever works.

Here's the data:

```
Region,Quarter,Product Category,Revenue ($K),Units Sold,Returns
Northeast,Q1,Electronics,842,12400,310
Northeast,Q1,Apparel,456,28900,1445
Northeast,Q1,Home & Garden,318,9200,184
Northeast,Q2,Electronics,910,13200,264
Northeast,Q2,Apparel,523,31500,945
Northeast,Q2,Home & Garden,387,10800,216
Northeast,Q3,Electronics,876,12800,384
Northeast,Q3,Apparel,612,35200,1056
Northeast,Q3,Home & Garden,445,12100,242
Northeast,Q4,Electronics,1205,17800,534
Northeast,Q4,Apparel,892,48600,1944
Northeast,Q4,Home & Garden,534,14200,284
Southeast,Q1,Electronics,634,9800,294
Southeast,Q1,Apparel,567,34200,1710
Southeast,Q1,Home & Garden,423,12800,256
Southeast,Q2,Electronics,712,10600,212
Southeast,Q2,Apparel,634,36800,1104
Southeast,Q2,Home & Garden,489,14200,284
Southeast,Q3,Electronics,698,10200,306
Southeast,Q3,Apparel,723,40100,1203
Southeast,Q3,Home & Garden,512,14800,296
Southeast,Q4,Electronics,945,14200,426
Southeast,Q4,Apparel,1034,55800,2232
Southeast,Q4,Home & Garden,612,16800,336
West,Q1,Electronics,1123,16200,486
West,Q1,Apparel,345,19800,990
West,Q1,Home & Garden,234,6800,136
West,Q2,Electronics,1245,17800,356
West,Q2,Apparel,398,22400,672
West,Q2,Home & Garden,278,7600,152
West,Q3,Electronics,1189,17200,516
West,Q3,Apparel,467,25600,768
West,Q3,Home & Garden,312,8400,168
West,Q4,Electronics,1567,22400,672
West,Q4,Apparel,678,36200,1448
West,Q4,Home & Garden,389,10200,204
Midwest,Q1,Electronics,523,8200,246
Midwest,Q1,Apparel,412,25600,1280
Midwest,Q1,Home & Garden,289,8800,176
Midwest,Q2,Electronics,578,8800,176
Midwest,Q2,Apparel,467,28200,846
Midwest,Q2,Home & Garden,334,9600,192
Midwest,Q3,Electronics,556,8600,258
Midwest,Q3,Apparel,534,30800,924
Midwest,Q3,Home & Garden,367,10200,204
Midwest,Q4,Electronics,745,11400,342
Midwest,Q4,Apparel,778,42200,1688
Midwest,Q4,Home & Garden,445,12400,248
```

The main thing the execs care about is understanding which regions and
categories are driving growth and where we should focus next year. They
also want to know about the return rate situation — it's been a concern.

Just need something clean that tells the story. Don't need anything
too fancy, they just want to quickly see what's going on.
