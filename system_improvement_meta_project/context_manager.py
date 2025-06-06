#!/usr/bin/env python3
"""
Persistent Memory & Context Management System
============================================

Bu sistem context limitleri ve session kesintileri sorununu çözer.
Seamless conversation continuity ve knowledge persistence sağlar.

Özellikler:
- Session state persistence
- Knowledge base integration
- Context compression intelligence
- Automated session resume
- Memory management intelligence
- Cross-session knowledge transfer

Kullanım:
    manager = ContextManager()
    manager.save_session_state()
    manager.resume_session()
"""

import os
import json
import pickle
import hashlib
import datetime
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import sqlite3

@dataclass
class SessionState:
    """Session state data structure"""
    session_id: str
    timestamp: str
    project_name: str
    current_tasks: List[str]
    completed_tasks: List[str]
    active_files: List[str]
    conversation_summary: str
    context_data: Dict[str, Any]
    user_preferences: Dict[str, Any]
    system_state: Dict[str, Any]
    knowledge_points: List[str]

@dataclass
class MemoryEntry:
    """Memory entry for knowledge base"""
    id: str
    timestamp: str
    content: str
    category: str
    importance: int  # 1-10
    tags: List[str]
    related_sessions: List[str]

class ContextManager:
    """
    Ana Context Management sistemi
    Session persistence, knowledge management ve intelligent resume sağlar
    """
    
    def __init__(self, project_name: str = "YAPYOS_v2"):
        self.project_name = project_name
        self.data_dir = Path("context_data")
        self.db_path = self.data_dir / "memory.db"
        
        # Directory setup
        self.data_dir.mkdir(exist_ok=True)
        (self.data_dir / "sessions").mkdir(exist_ok=True)
        (self.data_dir / "exports").mkdir(exist_ok=True)
        
        # Logging setup
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/context_manager.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self._init_database()
        
        # Current session
        self.current_session = None
        self.session_id = None
        
        self.logger.info("Context Manager initialized successfully")

    def _init_database(self):
        """Initialize SQLite database for persistent memory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    project_name TEXT,
                    status TEXT,
                    summary TEXT,
                    data_file TEXT
                )
            ''')
            
            # Memory entries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory_entries (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    content TEXT,
                    category TEXT,
                    importance INTEGER,
                    tags TEXT,
                    related_sessions TEXT
                )
            ''')
            
            # Knowledge graph table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_graph (
                    id TEXT PRIMARY KEY,
                    subject TEXT,
                    predicate TEXT,
                    object TEXT,
                    confidence REAL,
                    timestamp TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
            self.logger.info("Database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Database initialization error: {e}")

    def create_session(self, context_data: Dict[str, Any] = None) -> str:
        """Yeni session oluştur"""
        self.session_id = hashlib.md5(
            f"{self.project_name}_{datetime.datetime.now()}".encode()
        ).hexdigest()[:12]
        
        # Current project state'i analiz et
        current_tasks = self._analyze_current_tasks()
        completed_tasks = self._analyze_completed_tasks()
        active_files = self._analyze_active_files()
        
        self.current_session = SessionState(
            session_id=self.session_id,
            timestamp=datetime.datetime.now().isoformat(),
            project_name=self.project_name,
            current_tasks=current_tasks,
            completed_tasks=completed_tasks,
            active_files=active_files,
            conversation_summary="",
            context_data=context_data or {},
            user_preferences={},
            system_state=self._capture_system_state(),
            knowledge_points=[]
        )
        
        self.logger.info(f"New session created: {self.session_id}")
        return self.session_id

    def _analyze_current_tasks(self) -> List[str]:
        """Current active tasks'leri analiz et"""
        tasks = []
        
        try:
            # ai_todo_list.md'den active tasks'leri oku
            todo_file = "ai_todo_list.md"
            if os.path.exists(todo_file):
                with open(todo_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Active tasks section'ı parse et
                lines = content.split('\n')
                in_active_section = False
                
                for line in lines:
                    if "ACTIVE STRATEGIC TASKS" in line:
                        in_active_section = True
                        continue
                    elif line.startswith("##") and in_active_section:
                        break
                    elif in_active_section and line.strip().startswith("####"):
                        task = line.replace("####", "").strip()
                        if task:
                            tasks.append(task)
                            
        except Exception as e:
            self.logger.warning(f"Task analysis error: {e}")
        
        return tasks

    def _analyze_completed_tasks(self) -> List[str]:
        """Completed tasks'leri analiz et"""
        tasks = []
        
        try:
            # task_progress.md'den completed tasks'leri oku
            progress_file = "task_progress.md"
            if os.path.exists(progress_file):
                with open(progress_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Completed tasks section'ı parse et
                lines = content.split('\n')
                in_completed_section = False
                
                for line in lines:
                    if "TAMAMLANAN GÖREVLER" in line:
                        in_completed_section = True
                        continue
                    elif line.startswith("##") and in_completed_section:
                        break
                    elif in_completed_section and line.strip().startswith("###"):
                        task = line.replace("###", "").strip()
                        if "✅" in task:
                            tasks.append(task.replace("✅", "").strip())
                            
        except Exception as e:
            self.logger.warning(f"Completed task analysis error: {e}")
        
        return tasks

    def _analyze_active_files(self) -> List[str]:
        """Active project files'ları analiz et"""
        files = []
        
        try:
            # Python files
            python_files = list(Path(".").glob("*.py"))
            files.extend([str(f) for f in python_files])
            
            # Markdown files
            md_files = list(Path(".").glob("*.md"))
            files.extend([str(f) for f in md_files])
            
            # JSON config files
            json_files = list(Path(".").glob("*.json"))
            files.extend([str(f) for f in json_files])
            
        except Exception as e:
            self.logger.warning(f"File analysis error: {e}")
        
        return files[:20]  # Limit to prevent overwhelming

    def _capture_system_state(self) -> Dict[str, Any]:
        """Current system state'i yakala"""
        state = {
            "working_directory": os.getcwd(),
            "python_version": "3.9+",
            "timestamp": datetime.datetime.now().isoformat(),
            "project_structure": {
                "total_files": len(list(Path(".").glob("*"))),
                "python_scripts": len(list(Path(".").glob("*.py"))),
                "markdown_docs": len(list(Path(".").glob("*.md"))),
            }
        }
        
        # Git status if available
        try:
            import subprocess
            result = subprocess.run(['git', 'status', '--short'], 
                                  capture_output=True, text=True)
            state["git_status"] = result.stdout
        except:
            state["git_status"] = "Not available"
        
        return state

    def save_session_state(self, conversation_summary: str = "", 
                          knowledge_points: List[str] = None) -> bool:
        """Current session state'i kaydet"""
        if not self.current_session:
            self.logger.warning("No active session to save")
            return False
        
        try:
            # Update session data
            self.current_session.conversation_summary = conversation_summary
            self.current_session.knowledge_points = knowledge_points or []
            self.current_session.timestamp = datetime.datetime.now().isoformat()
            
            # Save to file
            session_file = self.data_dir / "sessions" / f"{self.session_id}.json"
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.current_session), f, indent=2, ensure_ascii=False)
            
            # Save to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO sessions 
                (session_id, timestamp, project_name, status, summary, data_file)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.session_id,
                self.current_session.timestamp,
                self.project_name,
                "active",
                conversation_summary,
                str(session_file)
            ))
            
            conn.commit()
            conn.close()
            
            # Save knowledge points
            if knowledge_points:
                self._save_knowledge_points(knowledge_points)
            
            self.logger.info(f"Session state saved: {self.session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Session save error: {e}")
            return False

    def _save_knowledge_points(self, knowledge_points: List[str]):
        """Knowledge points'leri memory'ye kaydet"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for point in knowledge_points:
                memory_id = hashlib.md5(point.encode()).hexdigest()[:12]
                
                cursor.execute('''
                    INSERT OR REPLACE INTO memory_entries
                    (id, timestamp, content, category, importance, tags, related_sessions)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    memory_id,
                    datetime.datetime.now().isoformat(),
                    point,
                    "knowledge_point",
                    7,  # High importance
                    json.dumps(["session_knowledge"]),
                    json.dumps([self.session_id])
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Knowledge save error: {e}")

    def resume_session(self, session_id: str = None) -> Optional[SessionState]:
        """Session'ı resume et"""
        if session_id is None:
            session_id = self._get_latest_session_id()
        
        if not session_id:
            self.logger.warning("No session to resume")
            return None
        
        try:
            session_file = self.data_dir / "sessions" / f"{session_id}.json"
            
            if not session_file.exists():
                self.logger.error(f"Session file not found: {session_id}")
                return None
            
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            self.current_session = SessionState(**session_data)
            self.session_id = session_id
            
            self.logger.info(f"Session resumed: {session_id}")
            return self.current_session
            
        except Exception as e:
            self.logger.error(f"Session resume error: {e}")
            return None

    def _get_latest_session_id(self) -> Optional[str]:
        """En son session ID'yi al"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT session_id FROM sessions 
                WHERE project_name = ? 
                ORDER BY timestamp DESC 
                LIMIT 1
            ''', (self.project_name,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
            
        except Exception as e:
            self.logger.error(f"Latest session query error: {e}")
            return None

    def generate_context_summary(self) -> str:
        """Current context için intelligent summary oluştur"""
        if not self.current_session:
            return "No active session"
        
        summary_parts = []
        
        # Project overview
        summary_parts.append(f"📋 **Project**: {self.project_name}")
        summary_parts.append(f"🕒 **Session**: {self.session_id}")
        
        # Active tasks
        if self.current_session.current_tasks:
            summary_parts.append(f"\n🎯 **Active Tasks** ({len(self.current_session.current_tasks)}):")
            for task in self.current_session.current_tasks[:3]:  # Top 3
                summary_parts.append(f"  • {task}")
        
        # Completed tasks
        if self.current_session.completed_tasks:
            summary_parts.append(f"\n✅ **Completed** ({len(self.current_session.completed_tasks)}):")
            for task in self.current_session.completed_tasks[-3:]:  # Recent 3
                summary_parts.append(f"  • {task}")
        
        # Key files
        if self.current_session.active_files:
            summary_parts.append(f"\n📁 **Key Files** ({len(self.current_session.active_files)}):")
            for file in self.current_session.active_files[:5]:  # Top 5
                summary_parts.append(f"  • {file}")
        
        # Conversation summary
        if self.current_session.conversation_summary:
            summary_parts.append(f"\n💬 **Last Conversation**:")
            summary_parts.append(f"  {self.current_session.conversation_summary}")
        
        return "\n".join(summary_parts)

    def export_session_resume_guide(self, session_id: str = None) -> str:
        """Session resume guide export et"""
        if session_id is None:
            session_id = self.session_id
        
        if not session_id:
            return "No session to export"
        
        try:
            session = self.resume_session(session_id) if session_id != self.session_id else self.current_session
            
            if not session:
                return "Session not found"
            
            guide = f"""# Session Resume Guide
# Session ID: {session.session_id}
# Project: {session.project_name}
# Timestamp: {session.timestamp}

## 🎯 ACTIVE TASKS
{chr(10).join(f"- {task}" for task in session.current_tasks)}

## ✅ COMPLETED TASKS  
{chr(10).join(f"- {task}" for task in session.completed_tasks)}

## 📁 ACTIVE FILES
{chr(10).join(f"- {file}" for file in session.active_files)}

## 💬 CONVERSATION CONTEXT
{session.conversation_summary}

## 🧠 KEY KNOWLEDGE POINTS
{chr(10).join(f"- {point}" for point in session.knowledge_points)}

## 🔄 TO RESUME SESSION:
```python
from context_manager import ContextManager
manager = ContextManager("{session.project_name}")
session = manager.resume_session("{session.session_id}")
summary = manager.generate_context_summary()
print(summary)
```
"""
            
            # Export to file
            export_file = self.data_dir / "exports" / f"resume_guide_{session_id}.md"
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write(guide)
            
            self.logger.info(f"Resume guide exported: {export_file}")
            return guide
            
        except Exception as e:
            self.logger.error(f"Export error: {e}")
            return f"Export failed: {e}"

    def search_memory(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """Memory'de search yap"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM memory_entries 
                WHERE content LIKE ? 
                ORDER BY importance DESC, timestamp DESC 
                LIMIT ?
            ''', (f"%{query}%", limit))
            
            results = cursor.fetchall()
            conn.close()
            
            entries = []
            for row in results:
                entry = MemoryEntry(
                    id=row[0],
                    timestamp=row[1], 
                    content=row[2],
                    category=row[3],
                    importance=row[4],
                    tags=json.loads(row[5]) if row[5] else [],
                    related_sessions=json.loads(row[6]) if row[6] else []
                )
                entries.append(entry)
            
            return entries
            
        except Exception as e:
            self.logger.error(f"Memory search error: {e}")
            return []

    def get_session_statistics(self) -> Dict[str, Any]:
        """Session istatistiklerini getir"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total sessions
            cursor.execute('SELECT COUNT(*) FROM sessions WHERE project_name = ?', 
                         (self.project_name,))
            total_sessions = cursor.fetchone()[0]
            
            # Total memory entries
            cursor.execute('SELECT COUNT(*) FROM memory_entries')
            total_memories = cursor.fetchone()[0]
            
            # Recent activity
            cursor.execute('''
                SELECT COUNT(*) FROM sessions 
                WHERE project_name = ? AND timestamp > datetime('now', '-7 days')
            ''', (self.project_name,))
            recent_sessions = cursor.fetchone()[0]
            
            conn.close()
            
            current_session_info = {}
            if self.current_session:
                current_session_info = {
                    "session_id": self.session_id,
                    "active_tasks": len(self.current_session.current_tasks),
                    "completed_tasks": len(self.current_session.completed_tasks),
                    "active_files": len(self.current_session.active_files),
                    "knowledge_points": len(self.current_session.knowledge_points)
                }
            
            return {
                "total_sessions": total_sessions,
                "total_memories": total_memories,
                "recent_sessions": recent_sessions,
                "current_session": current_session_info,
                "data_directory": str(self.data_dir),
                "database_size": os.path.getsize(self.db_path) if self.db_path.exists() else 0
            }
            
        except Exception as e:
            self.logger.error(f"Statistics error: {e}")
            return {"error": str(e)}


def main():
    """Test/demo function"""
    print("🧠 Context Manager Test")
    print("=" * 50)
    
    # Manager'ı initialize et
    manager = ContextManager("YAPYOS_v2_Test")
    
    # Yeni session oluştur
    session_id = manager.create_session({
        "test_mode": True,
        "demo_context": "Context management testing"
    })
    
    print(f"\n🆔 Session Created: {session_id}")
    
    # Context summary oluştur
    summary = manager.generate_context_summary()
    print(f"\n📋 Context Summary:")
    print(summary)
    
    # Session save et
    knowledge_points = [
        "Context management is crucial for AI continuity",
        "Session persistence enables seamless collaboration",
        "Memory management reduces repeated explanations"
    ]
    
    success = manager.save_session_state(
        conversation_summary="Testing context management functionality",
        knowledge_points=knowledge_points
    )
    
    print(f"\n💾 Session Saved: {'✅' if success else '❌'}")
    
    # Resume guide export
    guide = manager.export_session_resume_guide()
    print(f"\n📄 Resume Guide Generated:")
    print(guide[:300] + "..." if len(guide) > 300 else guide)
    
    # Statistics
    stats = manager.get_session_statistics()
    print(f"\n📊 Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\n✅ Context Manager ready for operation!")
    
    return manager


if __name__ == "__main__":
    manager = main() 