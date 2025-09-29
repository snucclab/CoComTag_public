import pandas as pd
import os
from collections import Counter
import random
import glob

base_dirs = ['result/dataname'] # modify to the name of your data
run_files = ['run0', 'run1', 'run2'] # the result of LLM_label_with_kappa_subfacet. The experiment were run 3 times
all_comparison_stats = []
detailed_decisions = []

random.seed(42)

output_dir = 'merge_result'
os.makedirs(output_dir, exist_ok=True)


for base_dir in base_dirs:
    run0_files = glob.glob(os.path.join(base_dir, 'run0_Team*.csv')) # might have to modify to your save format
    team_names = [os.path.basename(f).replace('run0_', '').replace('.csv', '') for f in run0_files]

    for team in team_names:
        try:
            dfs = []
            for run in run_files:
                path = os.path.join(base_dir, f'{run}_{team}.csv')
                df = pd.read_csv(path)
                df['utterance_id'] = df.index
                dfs.append(df)

            merged_df = pd.DataFrame({
                'utterance_id': dfs[0]['utterance_id'],
                'utterance': dfs[0]['content'],
                'pred1': dfs[0]['pred'],
                'pred2': dfs[1]['pred'],
                'pred3': dfs[2]['pred'],
            })

            all_same = 0
            two_same = 0
            all_diff = 0

            final_labels = []
            decision_details = []

            for idx, row in merged_df.iterrows():
                preds = [row['pred1'], row['pred2'], row['pred3']]
                count = Counter(preds)
                most_common = count.most_common()

                if len(count) == 1:
                    final = preds[0]
                    all_same += 1
                    decision_type = 'all_same'
                elif most_common[0][1] == 2:
                    final = most_common[0][0]
                    two_same += 1
                    decision_type = 'two_same'
                else:
                    final = random.choice(preds)
                    all_diff += 1
                    decision_type = 'all_diff'

                final_labels.append(final)
                decision_details.append({
                    'utterance': row['utterance'],
                    'pred1': row['pred1'],
                    'pred2': row['pred2'],
                    'pred3': row['pred3'],
                    'final_label': final,
                    'decision_type': decision_type,
                    'team': team,
                    'source': base_dir
                })

      
            team_dir = os.path.join(output_dir, os.path.basename(base_dir))
            os.makedirs(team_dir, exist_ok=True)
            result_df = pd.DataFrame({
                'utterance_id': merged_df['utterance_id'],
                'content': dfs[0]['content'],
                'username': dfs[0]['username'],
                'final_label': final_labels
            })
            result_df.to_csv(os.path.join(team_dir, f'{team}.csv'), index=False)

            
            total = len(merged_df)
            all_comparison_stats.append({
                'source': os.path.basename(base_dir),
                'team': team,
                'total': total,
                'all_same': all_same,
                'two_same': two_same,
                'all_diff': all_diff,
                'percent_all_same': round(all_same / total * 100, 2),
                'percent_two_same': round(two_same / total * 100, 2),
                'percent_all_diff': round(all_diff / total * 100, 2),
            })

            detailed_decisions.extend(decision_details)

        except Exception as e:
            print(f"Error - {base_dir}/{team}: {e}")

stats_df = pd.DataFrame(all_comparison_stats)
detailed_df = pd.DataFrame(detailed_decisions)
stats_df.to_csv('merge_result/team_comparison_summary.csv', index=False)
detailed_df.to_csv('merge_result/detailed_decision_log.csv', index=False)

print(stats_df)
print(detailed_df)


if not stats_df.empty:
    total_all = stats_df['total'].sum()
    total_all_same = stats_df['all_same'].sum()
    total_two_same = stats_df['two_same'].sum()
    total_all_diff = stats_df['all_diff'].sum()

    percent_all_same = round((total_all_same / total_all) * 100, 2)
    percent_two_same = round((total_two_same / total_all) * 100, 2)
    percent_all_diff = round((total_all_diff / total_all) * 100, 2)

    summary = {
        'total_predictions': total_all,
        'total_all_same': total_all_same,
        'percent_all_same': percent_all_same,
        'total_two_same': total_two_same,
        'percent_two_same': percent_two_same,
        'total_all_diff': total_all_diff,
        'percent_all_diff': percent_all_diff,
    }

    overall_df = pd.DataFrame([summary])
    print(overall_df)