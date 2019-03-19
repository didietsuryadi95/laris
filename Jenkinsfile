//maintener : DevOps < devops@staff.gramedia.com >

pipeline
{
    environment
    {
        PROJECT = 'ansible:operation'
        ECRURL = 'https://396676188700.dkr.ecr.ap-southeast-1.amazonaws.com'
        ECRCRED = 'ecr:ap-southeast-1:ecrcred'
        GIT_BRANCH_OR_TAG = sh(returnStdout: true, script:
'''\
     #!/bin/bash -e
     GIT_REMOTE=$(git remote)
     if git rev-parse --verify -q refs/remotes/${GIT_REMOTE}/${GIT_BRANCH}^{} | grep -q ${GIT_COMMIT}
       then echo branch
       exit 0
     elif git rev-parse --verify -q refs/tags/${GIT_BRANCH}^{} | grep -q ${GIT_COMMIT}
       then echo tag
       exit 0
     else echo unknown
       exit 0
     fi
'''.stripIndent()).trim()
    }
//Agent use Any
    agent any

//Parameters input
    parameters
    {
        string(defaultValue: "", description: 'Ansible Vault Password to Decrypt Vault variables', name: 'ansible_vault_pass')
    }
    stages
    {

//Stage Develop

        stage('Ansible Deploy to dev-testimo.gramedia.io [Develop]')
        {
            when
            {
                branch 'develop'
            }
            steps
            {
                script
                {
                    def cmd = """
                    PIPE=\$(mktemp -u);
                    mkfifo \$PIPE;
                    (echo '${params.ansible_vault_pass}' >\$PIPE &);
                    ansible-playbook ./deploy/omnibus.yml -i ./deploy/environments/develop --extra-vars "app_role_sphinx=develop" --vault-password-file=\$PIPE || (
                    RC=\$?;
                    rm \$PIPE;
                    exit \$RC
                    )
                    rm \$PIPE;
                    """
                    sh cmd
                }
            }
        }

//Stage Staging

        stage('Ansible Deploy to staging.testimobysb.com [Staging]')
        {
            when
            {
                branch 'master'
            }
            steps
            {
                script
                {
                    def cmd = """
                    PIPE=\$(mktemp -u);
                    mkfifo \$PIPE;
                    (echo '${params.ansible_vault_pass}' >\$PIPE &);
                    ansible-playbook ./deploy/omnibus.yml -i ./deploy/environments/staging --extra-vars "app_role_sphinx=staging" --vault-password-file=\$PIPE || (
                    RC=\$?;
                    rm \$PIPE;
                    exit \$RC
                    )
                    rm \$PIPE;
                    """
                    sh cmd
                }
            }
        }

//Stage Production

        stage('Ansible Deploy to testimobysb.com [Production]')
        {
            when
            {
                expression
                {
                    env.GIT_BRANCH_OR_TAG == 'tag'
                }
            }
            steps
            {
            script
            {
                def branch_name = env.BRANCH_NAME.replaceAll('\\/','-')
                def cmd = """
                PIPE=\$(mktemp -u);
                mkfifo \$PIPE;
                (echo '${testimo}' >\$PIPE &);
                ansible-playbook ./deploy/omnibus.yml -i ./deploy/environments/production --extra-vars 'repo_ref=${branch_name}' --private-key=~/.ssh/bhisma_id_rsa --vault-password-file=\$PIPE || (
                RC=\$?;
                rm \$PIPE;
                exit \$RC
                )
                rm \$PIPE;
                """
                sh cmd
            }
            }
        }
    }
// After pipeline done
    post {
        always {
            cleanWs()
        }
        failure {
            echo 'build-failed'
        }
        success {
            echo 'build-done'
        }
    }
}
