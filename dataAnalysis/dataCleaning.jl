using Pkg
Pkg.activate(".")

using CSV, DataFrames, Glob

function consolidate_data(policies::Vector{String}, scenarios::Vector{String}, deployment_types::Vector{String})
    base_dir = "./simOutput"
    save_path = "./dataAnalysis/consolidatedData.csv"
    columns_to_extract = ["scenario_cls", "AdoptingPolicyCls", "BasePolicyCls", "outcome", "percent_adopt", "value", "yerr"]
    
    consolidated_df = DataFrame() 

    policy_filter_map = Dict(
        "AS-Cones" => "OnlyToCustomers",
        "ASPA" => "ROV",
        "PeerROV" => "BGP",
        "ROV" => "BGP",
        "ROVPPV2Lite" => "ROVPPV2Lite",
        "ROVPPV1Lite" => "ROVPPV1Lite",
        "ROVPPV2ImprovedLite" => "ROVPPV2ImprovedLite"
    )

    for policy in policies
        for scenario in scenarios
            if (policy == "ROVPPV2Lite" || policy == "ROVPPV1Lite" || policy == "ROVPPV2ImprovedLite") && scenario == "AccidentalRouteLeak"
                continue
            end
            for deployment_type in deployment_types
                dir_path = joinpath(base_dir, "$(policy)$(scenario)$(deployment_type)")
                csv_files = glob("*.csv", dir_path)
                
                if isempty(csv_files)
                    println("No CSV files found in: $dir_path")
                end

                for file in csv_files
                    df = CSV.read(file, DataFrame)

                    rename!(df, string.(names(df)) .|> strip)

                    missing_cols = filter(c -> !(c in names(df)), columns_to_extract)
                    if isempty(missing_cols)
                        sub_df = select(df, columns_to_extract)

                        if scenario == "ForgedOriginSubPrefix"
                            sub_df[!, :scenario_cls] .= "ForgedOriginPrefix"
                        end

                        if policy == "AS-Cones"
                            sub_df[!, :AdoptingPolicyCls] .= "AS-Cones"
                        end

                        policy_cls_filter = policy_filter_map[policy]
                        sub_df = filter(row -> row[:PolicyCls] == policy_cls_filter, sub_df)

                        sub_df[!, :deployment_type] = fill(deployment_type, nrow(sub_df))

                        consolidated_df = vcat(consolidated_df, sub_df)
                    else
                        println("Missing columns in $(file): $(missing_cols)")
                        println("Available columns: $(names(df))")
                    end
                end
            end
        end
    end

    if isempty(consolidated_df)
        println("No data was added to the DataFrame.")
    else
        CSV.write(save_path, consolidated_df)
        println("Data consolidated and saved to $save_path")
    end
    
    return consolidated_df
end


policies = ["ROV", "PeerROV", "ASPA", "AS-Cones", "ROVPPV2Lite", "ROVPPV1Lite", "ROVPPV2ImprovedLite"]
scenarios = ["PrefixHijack", "AccidentalRouteLeak", "SubprefixHijack", "ForgedOriginSubPrefix"]
deployment_types = ["STUBS", "MULTIHOMED", "INPUT_CLIQUE", "NoDeploymentType"]

result_df = consolidate_data(policies, scenarios, deployment_types)
