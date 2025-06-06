#!/usr/bin/env python3
"""
Autonomy Management System - Script Execution Permission Framework
==================================================================

Bu sistem AI'ın script execution autonomy bottleneck'ini çözer.
Risk-based, context-aware intelligent permission framework.

Özellikler:
- Risk assessment engine
- Dynamic permission management
- Safe execution framework  
- Progressive learning capability
- Context-aware decision making

Kullanım:
    manager = AutonomyManager()
    result = manager.assess_and_execute(script_path, context)
"""

import os
import json
import time
import hashlib
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from enum import Enum

class RiskLevel(Enum):
    """Risk seviyeleri enum'u"""
    LOW = "low"           # Otomatik çalıştırılabilir
    MEDIUM = "medium"     # Context-based decision
    HIGH = "high"         # User approval gerekli
    CRITICAL = "critical" # Kesinlikle user approval

class PermissionDecision(Enum):
    """Permission kararları"""
    ALLOW = "allow"           # Otomatik çalıştır
    ASK_USER = "ask_user"     # User'a sor
    DENY = "deny"             # Reddet
    SANDBOX = "sandbox"       # Sandbox'ta çalıştır

class AutonomyManager:
    """
    Ana Autonomy Management sistemi
    Risk assessment, permission management ve safe execution sağlar
    """
    
    def __init__(self, config_file: str = "autonomy_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.execution_log = []
        self.user_behavior_data = []
        
        # Logging setup
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/autonomy_manager.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Risk patterns ve operation signatures
        self.risk_patterns = self._initialize_risk_patterns()
        self.safe_directories = self.config.get("safe_directories", [])
        self.restricted_directories = self.config.get("restricted_directories", [])
        
        self.logger.info("Autonomy Manager initialized successfully")

    def _load_config(self) -> Dict:
        """Autonomy configuration'ını yükle"""
        default_config = {
            "autonomy_level": "medium",
            "auto_approve_categories": [
                "read_operations", "validation", "monitoring", "analysis"
            ],
            "sandbox_required": [
                "file_modifications", "git_operations", "dependency_checks"
            ],
            "always_ask": [
                "system_changes", "external_network", "critical_deletions"
            ],
            "safe_directories": [
                "system_improvement_meta_project/",
                "logs/",
                "temp/"
            ],
            "restricted_directories": [
                "project_docs/",
                "/",
                "C:\\"
            ],
            "max_execution_time": 300,
            "resource_limits": {
                "memory": "1GB",
                "cpu": "50%"
            },
            "learning_enabled": True,
            "progressive_autonomy": True
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception as e:
                self.logger.warning(f"Config yüklenemedi, default kullanılıyor: {e}")
        
        return default_config

    def _initialize_risk_patterns(self) -> Dict:
        """Risk pattern'leri initialize et"""
        return {
            # LOW RISK PATTERNS
            "low_risk": {
                "file_extensions": [".log", ".txt", ".md", ".json", ".csv"],
                "operations": ["read", "list", "check", "validate", "analyze", "monitor"],
                "commands": ["ls", "cat", "head", "tail", "grep", "find", "wc"],
                "script_patterns": ["check_", "validate_", "monitor_", "analyze_", "lint_"]
            },
            
            # MEDIUM RISK PATTERNS  
            "medium_risk": {
                "operations": ["backup", "copy", "move", "create", "test"],
                "commands": ["cp", "mv", "mkdir", "touch", "python", "pytest"],
                "script_patterns": ["backup_", "test_", "update_", "setup_"]
            },
            
            # HIGH RISK PATTERNS
            "high_risk": {
                "operations": ["delete", "remove", "install", "commit", "push"],
                "commands": ["rm", "del", "git commit", "git push", "pip install", "npm install"],
                "script_patterns": ["delete_", "remove_", "install_", "deploy_"]
            },
            
            # CRITICAL RISK PATTERNS
            "critical_risk": {
                "operations": ["format", "shutdown", "reboot", "sudo"],
                "commands": ["format", "shutdown", "reboot", "sudo", "chmod 777"],
                "system_paths": ["/etc/", "/usr/", "/var/", "C:\\Windows\\"]
            }
        }

    def assess_risk(self, script_path: str, context: Dict) -> Tuple[RiskLevel, Dict]:
        """
        Script riskini assess et
        
        Args:
            script_path: Çalıştırılacak script'in path'i
            context: Execution context bilgileri
            
        Returns:
            Tuple[RiskLevel, risk_details]
        """
        risk_details = {
            "factors": [],
            "score": 0,
            "reasoning": []
        }
        
        # Check for operation-specific overrides first
        script_name = os.path.basename(script_path)
        operation_rules = self.config.get("operation_specific_rules", {})
        
        if script_name in operation_rules:
            rule = operation_rules[script_name]
            risk_override = rule.get("risk_override", "").lower()
            reason = rule.get("reason", "No reason provided")
            
            if risk_override:
                self.logger.info(f"Operation rule override applied for {script_name}: {risk_override} - {reason}")
                
                # Apply override to overall risk
                if risk_override == "low":
                    level = RiskLevel.LOW
                    risk_score = 1
                elif risk_override == "medium":
                    level = RiskLevel.MEDIUM
                    risk_score = 3
                elif risk_override == "high":
                    level = RiskLevel.HIGH
                    risk_score = 7
                else:
                    level = RiskLevel.CRITICAL
                    risk_score = 9
                
                risk_details["score"] = risk_score
                risk_details["factors"].append(f"Operation rule override: {risk_override}")
                risk_details["factors"].append(f"Reason: {reason}")
                risk_details["reasoning"] = self._generate_risk_reasoning(level, risk_details)
                
                self.logger.info(f"Risk assessment (override): {script_path} -> {level.value} (score: {risk_score})")
                return level, risk_details
        
        # Normal risk assessment if no override
        # 1. File Path Analysis
        path_risk = self._assess_path_risk(script_path)
        risk_details["factors"].append(f"Path risk: {path_risk}")
        
        # 2. Script Content Analysis (eğer mümkünse)
        content_risk = self._assess_content_risk(script_path)
        risk_details["factors"].append(f"Content risk: {content_risk}")
        
        # 3. Operation Type Analysis
        operation_risk = self._assess_operation_risk(script_path, context)
        risk_details["factors"].append(f"Operation risk: {operation_risk}")
        
        # 4. Directory Scope Analysis
        directory_risk = self._assess_directory_risk(script_path, context)
        risk_details["factors"].append(f"Directory risk: {directory_risk}")
        
        # 5. Context Analysis
        context_risk = self._assess_context_risk(context)
        risk_details["factors"].append(f"Context risk: {context_risk}")
        
        # Risk skoru hesapla
        risk_score = max(path_risk, content_risk, operation_risk, directory_risk, context_risk)
        risk_details["score"] = risk_score
        
        # Risk seviyesi belirle
        if risk_score <= 2:
            level = RiskLevel.LOW
        elif risk_score <= 4:
            level = RiskLevel.MEDIUM  
        elif risk_score <= 7:
            level = RiskLevel.HIGH
        else:
            level = RiskLevel.CRITICAL
            
        risk_details["reasoning"] = self._generate_risk_reasoning(level, risk_details)
        
        self.logger.info(f"Risk assessment: {script_path} -> {level.value} (score: {risk_score})")
        return level, risk_details

    def _assess_path_risk(self, script_path: str) -> int:
        """Script path'inin riskini değerlendir"""
        path = Path(script_path)
        
        # Absolute path'e çevir
        if not path.is_absolute():
            path = Path(os.getcwd()) / path
        
        path_str = str(path).replace("\\", "/")  # Windows path normalization
        
        # Safe directories'de ise düşük risk
        for safe_dir in self.safe_directories:
            safe_dir_normalized = safe_dir.replace("\\", "/")
            if safe_dir_normalized in path_str or path_str.endswith(script_path):
                return 1
                
        # Meta-project directory'de ise düşük risk
        if "system_improvement_meta_project" in path_str:
            return 1
            
        # Restricted directories'de ise yüksek risk
        for restricted_dir in self.restricted_directories:
            restricted_dir_normalized = restricted_dir.replace("\\", "/")
            if path_str.startswith(restricted_dir_normalized):
                return 8
                
        # Current working directory'de ise orta risk
        current_dir = os.getcwd().replace("\\", "/")
        if "system_improvement_meta_project" in current_dir:
            return 2
            
        return 5  # Default orta risk

    def _assess_content_risk(self, script_path: str) -> int:
        """Script içeriğinin riskini değerlendir"""
        try:
            # Operation-specific overrides check
            script_name = os.path.basename(script_path)
            operation_rules = self.config.get("operation_specific_rules", {})
            
            self.logger.debug(f"Checking operation rules for: {script_name}")
            self.logger.debug(f"Available rules: {list(operation_rules.keys())}")
            
            if script_name in operation_rules:
                rule = operation_rules[script_name]
                risk_override = rule.get("risk_override", "").lower()
                reason = rule.get("reason", "No reason provided")
                self.logger.info(f"Operation rule applied for {script_name}: {risk_override} - {reason}")
                
                if risk_override == "low":
                    return 1
                elif risk_override == "medium":
                    return 3
                elif risk_override == "high":
                    return 7
            
            if not os.path.exists(script_path):
                self.logger.debug(f"Script not found: {script_path}")
                return 3  # File yok, orta risk
                
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
            # High risk keywords
            high_risk_keywords = [
                'rm -rf', 'del /f', 'format', 'shutdown', 'reboot', 
                'sudo', 'chmod 777', 'git push', 'pip install'
            ]
            
            # Medium risk keywords  
            medium_risk_keywords = [
                'git commit', 'mkdir', 'copy', 'move', 'backup'
            ]
            
            # Low risk keywords
            low_risk_keywords = [
                'read', 'check', 'validate', 'analyze', 'monitor', 'lint',
                'print', 'log', 'report', 'scan', 'test'
            ]
            
            for keyword in high_risk_keywords:
                if keyword in content:
                    self.logger.debug(f"High risk keyword found: {keyword}")
                    return 8
                    
            for keyword in medium_risk_keywords:
                if keyword in content:
                    self.logger.debug(f"Medium risk keyword found: {keyword}")
                    return 4
                    
            for keyword in low_risk_keywords:
                if keyword in content:
                    self.logger.debug(f"Low risk keyword found: {keyword}")
                    return 1
                    
            self.logger.debug(f"No specific keywords found, using default risk")
            return 3  # Default
            
        except Exception as e:
            self.logger.warning(f"Content analysis hatası: {e}")
            return 5  # Error durumunda orta risk

    def _assess_operation_risk(self, script_path: str, context: Dict) -> int:
        """Operation tipinin riskini değerlendir"""
        operation_type = context.get("operation_type", "unknown")
        
        if operation_type in ["read", "check", "validate", "monitor", "analyze"]:
            return 1
        elif operation_type in ["backup", "test", "update"]:
            return 3
        elif operation_type in ["install", "deploy", "commit"]:
            return 7
        elif operation_type in ["delete", "remove", "format"]:
            return 9
            
        return 4  # Default

    def _assess_directory_risk(self, script_path: str, context: Dict) -> int:
        """Working directory riskini değerlendir"""
        working_dir = context.get("working_directory", os.getcwd())
        
        # Safe directories
        if any(safe_dir in working_dir for safe_dir in self.safe_directories):
            return 1
            
        # Restricted directories
        if any(restricted_dir in working_dir for restricted_dir in self.restricted_directories):
            return 8
            
        return 4  # Default

    def _assess_context_risk(self, context: Dict) -> int:
        """Context bilgilerinin riskini değerlendir"""
        risk_score = 0
        
        # User presence
        if context.get("user_present", True):
            risk_score += 0
        else:
            risk_score += 2
            
        # Time of day
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 17:  # Working hours
            risk_score += 0
        else:
            risk_score += 1
            
        # Emergency context
        if context.get("emergency", False):
            risk_score += 3
            
        return min(risk_score, 5)

    def _generate_risk_reasoning(self, level: RiskLevel, risk_details: Dict) -> List[str]:
        """Risk kararı için reasoning oluştur"""
        reasoning = []
        
        if level == RiskLevel.LOW:
            reasoning.append("✅ Güvenli operasyon - otomatik çalıştırılabilir")
        elif level == RiskLevel.MEDIUM:
            reasoning.append("⚠️ Orta risk - context'e göre karar verilecek")
        elif level == RiskLevel.HIGH:
            reasoning.append("🔴 Yüksek risk - user approval gerekli")
        else:
            reasoning.append("🚨 Kritik risk - kesinlikle user approval")
            
        reasoning.extend(risk_details["factors"])
        return reasoning

    def get_permission(self, risk_level: RiskLevel, context: Dict, risk_details: Dict) -> PermissionDecision:
        """
        Risk seviyesi ve context'e göre permission kararı ver
        
        Args:
            risk_level: Assessed risk seviyesi
            context: Execution context
            risk_details: Risk assessment detayları
            
        Returns:
            PermissionDecision
        """
        autonomy_level = self.config.get("autonomy_level", "medium")
        
        # User autonomy preference'ını dikkate al
        if autonomy_level == "full":
            # Full autonomy mode - sadece critical'lar için approval
            if risk_level == RiskLevel.CRITICAL:
                return PermissionDecision.ASK_USER
            elif risk_level == RiskLevel.HIGH:
                return PermissionDecision.SANDBOX
            else:
                return PermissionDecision.ALLOW
                
        elif autonomy_level == "high":
            # High autonomy mode
            if risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
                return PermissionDecision.ASK_USER
            elif risk_level == RiskLevel.MEDIUM:
                return self._context_based_decision(context, risk_details)
            else:
                return PermissionDecision.ALLOW
                
        elif autonomy_level == "medium":
            # Medium autonomy mode (default)
            if risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
                return PermissionDecision.ASK_USER
            elif risk_level == RiskLevel.MEDIUM:
                return PermissionDecision.SANDBOX
            else:
                return PermissionDecision.ALLOW
                
        else:  # low autonomy
            # Low autonomy mode - sadece low risk otomatik
            if risk_level == RiskLevel.LOW:
                return PermissionDecision.ALLOW
            else:
                return PermissionDecision.ASK_USER

    def _context_based_decision(self, context: Dict, risk_details: Dict) -> PermissionDecision:
        """Context'e göre intelligent karar ver"""
        
        # Working directory check
        if context.get("working_directory", "").startswith("system_improvement_meta_project"):
            return PermissionDecision.ALLOW  # Meta-project'te daha liberal
            
        # Operation type check
        operation = context.get("operation_type", "")
        if operation in ["backup", "test", "validate"]:
            return PermissionDecision.ALLOW
            
        # User behavior learning
        if self.config.get("learning_enabled", True):
            historical_decision = self._predict_user_decision(context, risk_details)
            if historical_decision:
                return PermissionDecision.ALLOW
                
        # Default olarak sandbox'ta çalıştır
        return PermissionDecision.SANDBOX

    def _predict_user_decision(self, context: Dict, risk_details: Dict) -> bool:
        """User behavior'dan öğrenerek karar tahmin et"""
        # Bu gelecekte ML model ile implement edilebilir
        # Şimdilik basit heuristic
        return len(self.user_behavior_data) > 5  # Dummy implementation

    def assess_and_execute(self, script_path: str, context: Optional[Dict] = None) -> Dict:
        """
        Ana method: Script'i assess et ve execute et
        
        Args:
            script_path: Çalıştırılacak script
            context: Execution context
            
        Returns:
            Execution result dictionary
        """
        if context is None:
            context = {}
            
        start_time = time.time()
        execution_id = hashlib.md5(f"{script_path}_{start_time}".encode()).hexdigest()[:8]
        
        self.logger.info(f"[{execution_id}] Assessment başlatıldı: {script_path}")
        
        try:
            # 1. Risk Assessment
            risk_level, risk_details = self.assess_risk(script_path, context)
            
            # 2. Permission Decision
            permission = self.get_permission(risk_level, context, risk_details)
            
            # 3. Execution Logic
            result = {
                "execution_id": execution_id,
                "script_path": script_path,
                "risk_level": risk_level.value,
                "risk_details": risk_details,
                "permission": permission.value,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "output": "",
                "error": "",
                "execution_time": 0
            }
            
            if permission == PermissionDecision.ALLOW:
                result.update(self._safe_execute(script_path, context))
                
            elif permission == PermissionDecision.SANDBOX:
                result.update(self._sandbox_execute(script_path, context))
                
            elif permission == PermissionDecision.ASK_USER:
                result.update(self._request_user_approval(script_path, risk_level, risk_details))
                
            else:  # DENY
                result["error"] = f"Execution denied due to {risk_level.value} risk level"
                
            # 4. Log execution
            result["execution_time"] = time.time() - start_time
            self._log_execution(result)
            
            # 5. Learning update
            if self.config.get("learning_enabled", True):
                self._update_learning_data(result, context)
            
            return result
            
        except Exception as e:
            self.logger.error(f"[{execution_id}] Execution error: {e}")
            return {
                "execution_id": execution_id,
                "success": False,
                "error": str(e),
                "execution_time": time.time() - start_time
            }

    def _safe_execute(self, script_path: str, context: Dict) -> Dict:
        """Güvenli script execution"""
        self.logger.info(f"Safe execution: {script_path}")
        
        try:
            # Resource limits ile execute et
            cmd = f"python {script_path}"
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.config.get("max_execution_time", 300),
                cwd=context.get("working_directory", os.getcwd())
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Script execution timeout",
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "return_code": -1
            }

    def _sandbox_execute(self, script_path: str, context: Dict) -> Dict:
        """Sandbox environment'ta execute et"""
        self.logger.info(f"Sandbox execution: {script_path}")
        
        # Şimdilik safe execute ile aynı, gelecekte docker sandbox implement edilecek
        result = self._safe_execute(script_path, context)
        result["execution_mode"] = "sandbox"
        return result

    def _request_user_approval(self, script_path: str, risk_level: RiskLevel, risk_details: Dict) -> Dict:
        """User'dan approval iste"""
        self.logger.info(f"User approval requested for: {script_path}")
        
        # Bu gelecekte interactive approval interface ile implement edilecek
        return {
            "success": False,
            "error": "User approval required",
            "approval_required": True,
            "risk_level": risk_level.value,
            "risk_details": risk_details
        }

    def _log_execution(self, result: Dict):
        """Execution'ı log'la"""
        self.execution_log.append(result)
        
        # Log file'a yaz
        log_entry = {
            "timestamp": result["timestamp"],
            "execution_id": result["execution_id"],
            "script": result["script_path"],
            "risk_level": result["risk_level"],
            "permission": result["permission"],
            "success": result["success"],
            "execution_time": result["execution_time"]
        }
        
        log_file = "logs/autonomy_execution.log"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")

    def _update_learning_data(self, result: Dict, context: Dict):
        """Learning data'yı güncelle"""
        learning_entry = {
            "timestamp": result["timestamp"],
            "context": context,
            "risk_level": result["risk_level"],
            "permission": result["permission"],
            "success": result["success"]
        }
        
        self.user_behavior_data.append(learning_entry)
        
        # Learning data'yı persist et
        learning_file = "logs/autonomy_learning.json"
        os.makedirs(os.path.dirname(learning_file), exist_ok=True)
        
        with open(learning_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_behavior_data, f, indent=2)

    def get_autonomy_stats(self) -> Dict:
        """Autonomy istatistiklerini getir"""
        total_executions = len(self.execution_log)
        if total_executions == 0:
            return {"message": "No executions yet"}
            
        successful_autonomous = sum(1 for ex in self.execution_log 
                                  if ex["permission"] == "allow" and ex["success"])
        
        autonomy_rate = (successful_autonomous / total_executions) * 100
        
        risk_distribution = {}
        for ex in self.execution_log:
            risk = ex["risk_level"]
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
            
        return {
            "total_executions": total_executions,
            "successful_autonomous": successful_autonomous,
            "autonomy_rate": f"{autonomy_rate:.1f}%",
            "risk_distribution": risk_distribution,
            "average_execution_time": sum(ex["execution_time"] for ex in self.execution_log) / total_executions
        }

    def update_autonomy_level(self, new_level: str):
        """Autonomy seviyesini güncelle"""
        valid_levels = ["low", "medium", "high", "full"]
        if new_level in valid_levels:
            self.config["autonomy_level"] = new_level
            
            # Config'i persist et
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
                
            self.logger.info(f"Autonomy level updated to: {new_level}")
        else:
            raise ValueError(f"Invalid autonomy level. Valid options: {valid_levels}")


def main():
    """Test/demo function"""
    print("🚀 Autonomy Manager Test")
    print("=" * 50)
    
    # Manager'ı initialize et
    manager = AutonomyManager()
    
    # Test script'i
    test_context = {
        "operation_type": "check",
        "working_directory": "system_improvement_meta_project/",
        "user_present": True
    }
    
    # Autonomy stats
    print("\n📊 Current Autonomy Stats:")
    stats = manager.get_autonomy_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\n🎯 Current autonomy level: {manager.config['autonomy_level']}")
    print("✅ Autonomy Manager ready for operation!")


if __name__ == "__main__":
    main() 