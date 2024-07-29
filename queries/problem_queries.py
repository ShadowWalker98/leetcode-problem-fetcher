

def get_num_problems_query():
    categories = ''
    query = ''' query problemsetQuestionList {
  problemsetQuestionList: questionList(
    categorySlug: "''' + categories + '''"
    limit: ''' + str(1) + '''
    skip: ''' + str(0) + '''
    filters: {}
  ) {
    total: totalNum
  }
}
    '''
    return query


def get_problem_list(categories: str, skip: int, limit: int) -> str:
    query = '''
    query problemsetQuestionList
     { 
     problemsetQuestionList: questionList(
    categorySlug: "''' + categories + '''"
    limit: ''' + str(limit) + '''
    skip: ''' + str(skip) + '''
    filters: {}
  ) {
    total: totalNum
    questions: data {
      acRate
      difficulty
      freqBar
      frontendQuestionId: questionFrontendId
      isFavor
      paidOnly: isPaidOnly
      status
      title
      titleSlug
      topicTags {
        name
        id
        slug
      }
      hasSolution
      hasVideoSolution
    }
  }
}
'''
    return query

