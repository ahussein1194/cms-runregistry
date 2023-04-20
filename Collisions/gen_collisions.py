import runregistry
import json
import csv

# Create JSON dict for Collision runs.
json_logic_collisions = {
  "and": [
    # Specify beam conditions.
    {"==": [{"var": "lumisection.oms.beam1_present"}, True]},
    {"==": [{"var": "lumisection.oms.beam2_present"}, True]},
    {"==": [{"var": "lumisection.oms.beam1_stable"}, True]},
    {"==": [{"var": "lumisection.oms.beam2_stable"}, True]},

    # Specify magnetic field condition.
    #{"==": [{"var": "run.oms.b_field"}, 3.8]},

    # Specify energy range (comment out for all).
    #{">=": [{"var": "run.oms.energy"}, 6000]},
    #{"<=": [{"var": "run.oms.energy"}, 7000]},

    # Specify dataset name ["online", "/PromptReco/Collisions2023/DQM", "/Express/Collisions2023/DQM"].
    { "==": [{"var": "dataset.name"}, "/PromptReco/Collisions2023/DQM"]},

    # Specify run number range (comment out for all).
    #{">=": [{"var": "run.oms.run_number"}, 360075]},
    #{"<=": [{"var": "run.oms.run_number"}, 360225]},

    # Specify the criteria for a good json.
    {"==": [{ "var": "lumisection.rr.cms-cms" }, "GOOD"]},
    {"==": [{"var": "lumisection.rr.dt-dt"}, "GOOD"]},
    {"==": [{"var": "lumisection.rr.csc-csc"}, "GOOD"]},
    {"==": [{"var": "lumisection.rr.rpc-rpc"}, "GOOD"]},
    #{"==": [{"var": "lumisection.rr.muon-muon"}, "GOOD"]},
    #{"==": [{"var": "lumisection.rr.gem-gem"}, "GOOD"]},
    #{"==": [{"var": "lumisection.rr.lumi-lumi"}, "GOOD"]},

    # Specify the run duration (in seconds).
    {">=": [{"var": "run.oms.duration"}, 3000]},

    # Other parameters.
    #{"==": [{"var": "lumisection.oms.cms_active"}, True]},
    #{"==": [{"var": "lumisection.oms.dtm_ready"}, true]},
    #{"==": [{"var": "lumisection.oms.dtp_ready"}, true]},
    #{"==": [{"var": "lumisection.oms.dt0_ready"}, true]},
    #{"==": [{"var": "lumisection.oms.cscm_ready"}, True]},
    #{"==": [{"var": "lumisection.oms.cscp_ready"}, True]},
    #{"==": [{"var": "lumisection.oms.rpc_ready"}, True]},
  ]
}

# Create a json file for the above criteria.
#generated_json_collisions = runregistry.create_json(json_logic_collisions)
generated_json_collisions = runregistry.generate_json(json_logic_collisions)

# Create a json file for the runs.
with open('json_collisions.txt', mode='w', encoding='utf-8') as json_file:
#    #f.write(str(generated_json_collisions))
    json.dump(generated_json_collisions, json_file)

# Create a CSV file with the required runs info.
with open('CollisionRuns_info.csv', mode='w', newline='') as out_csvfile:
    # Create a CSV writer object.
    csv_writer = csv.writer(out_csvfile)
    # Write the header.
    out_csv_header = \
    ['Run number', 'Fill', 'Energy', 'Duration(hr)', 'End date', 'CMSSW_V', 'Era', 'JSON-List']
    csv_writer.writerow(out_csv_header)

    # Write the data to the out file row by row.
    for run_number, json_list in generated_json_collisions.items():
        oms_attr = runregistry.get_run(int(run_number))['oms_attributes']
        fill_number = oms_attr['fill_number']
        energy = oms_attr['energy']
        duration = round((oms_attr['duration'] / (60.*60.)), 2)
        end_time = oms_attr['end_time']
        cmssw_version = oms_attr['cmssw_version'] 
        era = oms_attr['era']
        row_data = [run_number, fill_number, energy, duration, end_time, cmssw_version, era, json_list]
        csv_writer.writerow(row_data)

# Test print.
#for run_number, json_list in generated_json_collisions.items():
#    print(f"{run_number}: {json_list}")
