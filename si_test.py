import spikeinterface.sorters as ss
import spikeinterface.extractors as se
import spikeinterface.full as si

# print('Installed sorters', ss.installed_sorters())

# local_path = si.download_dataset(remote_path='/home/ikharitonov/spikeinterface_datasets/ephy_testing_data/mearec/mearec_test_10s.h5')
local_path = '/home/ikharitonov/spikeinterface_datasets/ephy_testing_data/mearec/mearec_test_10s.h5'
recording, sorting_true = se.read_mearec(local_path)

sorting_IC = ss.run_ironclust(recording, docker_image="spikeinterface/ironclust-compiled-base:latest", verbose=True)
print("ironclust sorting",sorting_IC)
# sorting_KS3 = ss.run_kilosort3(recording, docker_image="spikeinterface/kilosort-compiled-base:latest")
# print("kilosort3 sorting",sorting_KS3)
# sorting_KS2_5 = ss.run_kilosort2_5(recording, docker_image="spikeinterface/kilosort2_5-compiled-base:latest")
# print("kilosort2.5 sorting",sorting_KS2_5)
# sorting_HDS = ss.run_hdsort(recording, docker_image="spikeinterface/hdsort-compiled-base:latest")
# print("HDsort sorting",sorting_HDS)

print('Units found by ironclust:', sorting_IC.get_unit_ids())
# print('Units found by kilosort3:', sorting_KS3.get_unit_ids())
# print('Units found by kilosort2.5:', sorting_KS2_5.get_unit_ids())
# print('Units found by HDsort:', sorting_HDS.get_unit_ids())
print('finished.')