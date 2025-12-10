"""
A/B Testing & Analytics Dashboard
Compare variants, track metrics, and optimize parameters for better results.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

logger = logging.getLogger(__name__)


class ABTest:
    """Represents an A/B test comparing parameter variants."""
    
    def __init__(
        self,
        test_id: str,
        name: str,
        variant_a: Dict[str, Any],
        variant_b: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.test_id = test_id
        self.name = name
        self.variant_a = variant_a
        self.variant_b = variant_b
        self.metadata = metadata or {}
        self.results = {'a': [], 'b': []}
        self.created_at = datetime.now().isoformat()
    
    def add_result(self, variant: str, score: float, feedback: Optional[str] = None):
        """Add a test result."""
        self.results[variant].append({
            'score': score,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_winner(self) -> Dict[str, Any]:
        """Determine winning variant."""
        if not self.results['a'] or not self.results['b']:
            return {'winner': None, 'reason': 'Insufficient data'}
        
        avg_a = statistics.mean([r['score'] for r in self.results['a']])
        avg_b = statistics.mean([r['score'] for r in self.results['b']])
        
        diff = abs(avg_a - avg_b)
        confidence = min(diff / max(avg_a, avg_b) * 100, 100) if max(avg_a, avg_b) > 0 else 0
        
        return {
            'winner': 'a' if avg_a > avg_b else 'b',
            'avg_score_a': avg_a,
            'avg_score_b': avg_b,
            'difference': diff,
            'confidence': confidence,
            'sample_size_a': len(self.results['a']),
            'sample_size_b': len(self.results['b'])
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'test_id': self.test_id,
            'name': self.name,
            'variant_a': self.variant_a,
            'variant_b': self.variant_b,
            'metadata': self.metadata,
            'results': self.results,
            'created_at': self.created_at,
            'winner': self.get_winner()
        }


class AnalyticsManager:
    """
    Manages A/B testing and analytics for parameter optimization.
    Tracks quality metrics, parameter performance, and generates insights.
    """
    
    def __init__(self, storage_path: str = './analytics'):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.tests: Dict[str, ABTest] = {}
        self.metrics_history: List[Dict[str, Any]] = []
        self._load_data()
    
    def _load_data(self):
        """Load stored tests and metrics."""
        # Load A/B tests
        tests_file = self.storage_path / 'ab_tests.json'
        if tests_file.exists():
            with open(tests_file, 'r') as f:
                data = json.load(f)
                for test_data in data:
                    test = ABTest(**test_data)
                    self.tests[test.test_id] = test
        
        # Load metrics history
        metrics_file = self.storage_path / 'metrics_history.json'
        if metrics_file.exists():
            with open(metrics_file, 'r') as f:
                self.metrics_history = json.load(f)
    
    def _save_tests(self):
        """Save A/B tests to disk."""
        tests_file = self.storage_path / 'ab_tests.json'
        with open(tests_file, 'w') as f:
            json.dump([t.to_dict() for t in self.tests.values()], f, indent=2)
    
    def _save_metrics(self):
        """Save metrics history to disk."""
        metrics_file = self.storage_path / 'metrics_history.json'
        with open(metrics_file, 'w') as f:
            json.dump(self.metrics_history, f, indent=2)
    
    def create_test(
        self,
        test_id: str,
        name: str,
        variant_a: Dict[str, Any],
        variant_b: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> ABTest:
        """Create a new A/B test."""
        test = ABTest(test_id, name, variant_a, variant_b, metadata)
        self.tests[test_id] = test
        self._save_tests()
        logger.info(f"Created A/B test: {name} ({test_id})")
        return test
    
    def add_test_result(
        self,
        test_id: str,
        variant: str,
        score: float,
        feedback: Optional[str] = None
    ):
        """Add a result to an A/B test."""
        test = self.tests.get(test_id)
        if not test:
            raise ValueError(f"Test not found: {test_id}")
        
        test.add_result(variant, score, feedback)
        self._save_tests()
    
    def get_test(self, test_id: str) -> Optional[ABTest]:
        """Get an A/B test."""
        return self.tests.get(test_id)
    
    def list_tests(self) -> List[Dict[str, Any]]:
        """List all A/B tests with summaries."""
        return [
            {
                'test_id': t.test_id,
                'name': t.name,
                'created_at': t.created_at,
                'results_count_a': len(t.results['a']),
                'results_count_b': len(t.results['b']),
                'winner': t.get_winner()
            }
            for t in self.tests.values()
        ]
    
    def record_metric(
        self,
        metric_name: str,
        value: float,
        parameters: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Record a quality metric."""
        metric = {
            'metric_name': metric_name,
            'value': value,
            'parameters': parameters,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        self.metrics_history.append(metric)
        self._save_metrics()
    
    def get_parameter_performance(
        self,
        parameter_name: str,
        metric_name: str = 'quality_score',
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze performance of different parameter values.
        
        Args:
            parameter_name: Name of parameter to analyze (e.g., 'lighting')
            metric_name: Metric to compare (e.g., 'quality_score')
            days: Number of days to analyze
        
        Returns:
            Performance analysis for each parameter value
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter recent metrics
        recent_metrics = [
            m for m in self.metrics_history
            if datetime.fromisoformat(m['timestamp']) >= cutoff_date
            and m['metric_name'] == metric_name
            and parameter_name in m['parameters']
        ]
        
        # Group by parameter value
        performance = defaultdict(list)
        for metric in recent_metrics:
            param_value = metric['parameters'][parameter_name]
            performance[param_value].append(metric['value'])
        
        # Calculate statistics
        analysis = {}
        for value, scores in performance.items():
            analysis[value] = {
                'count': len(scores),
                'avg_score': statistics.mean(scores),
                'median_score': statistics.median(scores),
                'std_dev': statistics.stdev(scores) if len(scores) > 1 else 0,
                'min_score': min(scores),
                'max_score': max(scores)
            }
        
        # Rank by average score
        ranked = sorted(
            analysis.items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        
        return {
            'parameter': parameter_name,
            'metric': metric_name,
            'days_analyzed': days,
            'total_samples': len(recent_metrics),
            'performance': dict(analysis),
            'ranking': [{'value': v, **stats} for v, stats in ranked]
        }
    
    def get_optimization_recommendations(
        self,
        current_parameters: Dict[str, Any],
        metric_name: str = 'quality_score'
    ) -> List[Dict[str, Any]]:
        """
        Generate parameter optimization recommendations based on historical data.
        
        Args:
            current_parameters: Current parameter set
            metric_name: Metric to optimize for
        
        Returns:
            List of recommended parameter changes
        """
        recommendations = []
        
        # Analyze each parameter
        for param_name in current_parameters.keys():
            if param_name in ['num_results', 'seed']:
                continue  # Skip non-quality parameters
            
            analysis = self.get_parameter_performance(param_name, metric_name)
            if not analysis['ranking']:
                continue
            
            # Get current value performance
            current_value = current_parameters[param_name]
            current_perf = analysis['performance'].get(current_value)
            
            # Get best performing value
            best_value = analysis['ranking'][0]['value']
            best_perf = analysis['ranking'][0]
            
            # Recommend if significantly better
            if current_perf and best_value != current_value:
                improvement = best_perf['avg_score'] - current_perf['avg_score']
                if improvement > 0.1:  # Significant improvement threshold
                    recommendations.append({
                        'parameter': param_name,
                        'current_value': current_value,
                        'recommended_value': best_value,
                        'current_avg_score': current_perf['avg_score'],
                        'recommended_avg_score': best_perf['avg_score'],
                        'expected_improvement': improvement,
                        'confidence': min(best_perf['count'] / 10, 1.0),  # Based on sample size
                        'reason': f"Historical data shows {best_value} performs {improvement:.2f} points better"
                    })
        
        # Sort by expected improvement
        recommendations.sort(key=lambda x: x['expected_improvement'], reverse=True)
        
        return recommendations
    
    def get_quality_trends(self, days: int = 30) -> Dict[str, Any]:
        """
        Get quality metric trends over time.
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Trend analysis with daily averages
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_metrics = [
            m for m in self.metrics_history
            if datetime.fromisoformat(m['timestamp']) >= cutoff_date
        ]
        
        # Group by date
        daily_scores = defaultdict(list)
        for metric in recent_metrics:
            date = datetime.fromisoformat(metric['timestamp']).date().isoformat()
            daily_scores[date].append(metric['value'])
        
        # Calculate daily averages
        trends = []
        for date, scores in sorted(daily_scores.items()):
            trends.append({
                'date': date,
                'avg_score': statistics.mean(scores),
                'count': len(scores),
                'min_score': min(scores),
                'max_score': max(scores)
            })
        
        # Calculate overall trend
        if len(trends) >= 2:
            first_week_avg = statistics.mean([t['avg_score'] for t in trends[:7]])
            last_week_avg = statistics.mean([t['avg_score'] for t in trends[-7:]])
            trend_direction = 'improving' if last_week_avg > first_week_avg else 'declining'
        else:
            trend_direction = 'insufficient_data'
        
        return {
            'days_analyzed': days,
            'total_generations': len(recent_metrics),
            'daily_trends': trends,
            'trend_direction': trend_direction,
            'overall_avg': statistics.mean([m['value'] for m in recent_metrics]) if recent_metrics else 0
        }


# Global instance
analytics_manager = AnalyticsManager()
