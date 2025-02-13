from modelscope.msdatasets import MsDataset
ds =  MsDataset.load('shaoxuan/SyntheticCards', subset_name='default', split='train')
print(ds)
for idx, data in enumerate(ds):
    print(idx, data)
