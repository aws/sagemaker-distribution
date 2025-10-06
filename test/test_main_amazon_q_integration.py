from __future__ import absolute_import

import os
import pytest
import tempfile
from unittest.mock import patch, MagicMock

pytestmark = pytest.mark.unit

from main import _copy_static_files
from utils import get_semver


class TestMainAmazonQIntegration:
    """Test cases for Amazon Q integration in main.py."""

    @patch('shutil.copy2')
    @patch('os.path.exists')
    def test_copy_static_files_with_amazon_q_script(self, mock_exists, mock_copy):
        """Test that Amazon Q artifacts script is copied when it exists."""
        # Mock file existence checks
        def exists_side_effect(path):
            if path.endswith('aws-cli-public-key.asc'):
                return True
            elif path.endswith('get_amazon_q_agentic_chat_artifacts.py'):
                return True
            elif path.endswith('dirs'):
                return True
            return False
        
        mock_exists.side_effect = exists_side_effect
        
        with tempfile.TemporaryDirectory() as temp_dir:
            base_version_dir = os.path.join(temp_dir, "base")
            new_version_dir = os.path.join(temp_dir, "new")
            os.makedirs(base_version_dir)
            os.makedirs(new_version_dir)
            
            # Call the function
            _copy_static_files(base_version_dir, new_version_dir, "2", "minor")
            
            # Verify that copy2 was called for Amazon Q script
            copy_calls = [call[0][0] for call in mock_copy.call_args_list]
            amazon_q_calls = [call for call in copy_calls if 'get_amazon_q_agentic_chat_artifacts.py' in call]
            assert len(amazon_q_calls) == 1
            assert amazon_q_calls[0] == "assets/get_amazon_q_agentic_chat_artifacts.py"

    @patch('shutil.copy2')
    @patch('os.path.exists')
    def test_copy_static_files_without_amazon_q_script(self, mock_exists, mock_copy):
        """Test that function works when Amazon Q artifacts script doesn't exist."""
        # Mock file existence checks - Amazon Q script doesn't exist
        def exists_side_effect(path):
            if path.endswith('aws-cli-public-key.asc'):
                return True
            elif path.endswith('get_amazon_q_agentic_chat_artifacts.py'):
                return False  # Script doesn't exist
            elif path.endswith('dirs'):
                return True
            return False
        
        mock_exists.side_effect = exists_side_effect
        
        with tempfile.TemporaryDirectory() as temp_dir:
            base_version_dir = os.path.join(temp_dir, "base")
            new_version_dir = os.path.join(temp_dir, "new")
            os.makedirs(base_version_dir)
            os.makedirs(new_version_dir)
            
            # Call the function - should not raise exception
            _copy_static_files(base_version_dir, new_version_dir, "2", "minor")
            
            # Verify that copy2 was not called for Amazon Q script
            copy_calls = [call[0][0] for call in mock_copy.call_args_list]
            amazon_q_calls = [call for call in copy_calls if 'get_amazon_q_agentic_chat_artifacts.py' in call]
            assert len(amazon_q_calls) == 0

    @patch('shutil.copy2')
    @patch('shutil.copytree')
    @patch('os.path.exists')
    def test_copy_static_files_v1_and_above(self, mock_exists, mock_copytree, mock_copy):
        """Test that dirs directory is copied for v1 and above."""
        # Mock file existence checks
        def exists_side_effect(path):
            if path.endswith('aws-cli-public-key.asc'):
                return True
            elif path.endswith('get_amazon_q_agentic_chat_artifacts.py'):
                return True
            elif path.endswith('dirs'):
                return True
            return False
        
        mock_exists.side_effect = exists_side_effect
        
        with tempfile.TemporaryDirectory() as temp_dir:
            base_version_dir = os.path.join(temp_dir, "base")
            new_version_dir = os.path.join(temp_dir, "new")
            os.makedirs(base_version_dir)
            os.makedirs(new_version_dir)
            
            # Test with major version >= 1
            _copy_static_files(base_version_dir, new_version_dir, "1", "minor")
            
            # Verify that copytree was called for dirs
            assert mock_copytree.called
            copytree_calls = [call[0] for call in mock_copytree.call_args_list]
            dirs_calls = [call for call in copytree_calls if any('dirs' in str(arg) for arg in call)]
            assert len(dirs_calls) > 0

    @patch('shutil.copy2')
    @patch('shutil.copytree')
    @patch('os.path.exists')
    def test_copy_static_files_v0(self, mock_exists, mock_copytree, mock_copy):
        """Test that dirs directory is not copied for v0."""
        # Mock file existence checks
        def exists_side_effect(path):
            if path.endswith('aws-cli-public-key.asc'):
                return True
            elif path.endswith('get_amazon_q_agentic_chat_artifacts.py'):
                return True
            elif path.endswith('dirs'):
                return True
            return False
        
        mock_exists.side_effect = exists_side_effect
        
        with tempfile.TemporaryDirectory() as temp_dir:
            base_version_dir = os.path.join(temp_dir, "base")
            new_version_dir = os.path.join(temp_dir, "new")
            os.makedirs(base_version_dir)
            os.makedirs(new_version_dir)
            
            # Test with major version 0
            _copy_static_files(base_version_dir, new_version_dir, "0", "minor")
            
            # Verify that copytree was not called (dirs should not be copied for v0)
            assert not mock_copytree.called

    @patch('os.path.relpath')
    @patch('shutil.copy2')
    @patch('os.path.exists')
    def test_copy_static_files_relative_paths(self, mock_exists, mock_copy, mock_relpath):
        """Test that relative paths are used correctly."""
        # Mock file existence checks
        mock_exists.return_value = True
        
        # Mock relpath to return predictable values
        def relpath_side_effect(path):
            if 'aws-cli-public-key.asc' in path:
                return 'base/aws-cli-public-key.asc'
            elif 'dirs' in path:
                return 'base/dirs'
            return path
        
        mock_relpath.side_effect = relpath_side_effect
        
        with tempfile.TemporaryDirectory() as temp_dir:
            base_version_dir = os.path.join(temp_dir, "base")
            new_version_dir = os.path.join(temp_dir, "new")
            os.makedirs(base_version_dir)
            os.makedirs(new_version_dir)
            
            _copy_static_files(base_version_dir, new_version_dir, "2", "minor")
            
            # Verify relpath was called for the Amazon Q script
            relpath_calls = [call[0][0] for call in mock_relpath.call_args_list]
            amazon_q_calls = [call for call in relpath_calls if 'get_amazon_q_agentic_chat_artifacts.py' in call]
            assert len(amazon_q_calls) == 1