# coding: utf-8
import boto3
session = boto3.Session(profile_name='python_automation')
dydbc = session.client('dynamodb')
dydbr = session.resource('dynamodb')
    
for table in dydbr.tables.all():
    print(table.name)

videos_table = dydbr.Table(name='videolyzer_videos_dev1')
print(videos_table.get_item(Key={'VideoName': 'city.mp4'}, ProjectionExpression='VideoMetadata')['Item'])

AttributeDefinitions=[{'AttributeName': 'testkeyp', 'AttributeType': 'S'}] 
KeySchema=[{'AttributeName': 'testkeyp', 'KeyType': 'HASH'}]
TableName='TestTable'
ProvisionedThroughtPut={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
params = {
    'TableName': TableName,
    'AttributeDefinitions': AttributeDefinitions,
    'KeySchema': KeySchema,
    'ProvisionedThroughput': ProvisionedThroughtPut
}
#dydbr.create_table(**params)
test_table = dydbr.Table(name='TestTable')
test_table.put_item(Item={'a': 1, 'b': 2, 'c': 3, 'testkeyp': 'Row1'})
print(test_table.get_item(Key={'testkeyp': 'Row1'})['Item'])
test_table.put_item(Item={'a': 2, 'b': 3, 'c': 4, 'testkeyp': 'Row1'})
print(test_table.get_item(Key={'testkeyp': 'Row1'})['Item'])
test_table.put_item(Item={'a': 2, 'b': 3, 'c': [1,2,3,4], 'testkeyp': 'Row1'})
print(test_table.get_item(Key={'testkeyp': 'Row1'})['Item'])
test_table.put_item(Item={'c': [5,6,7,8], 'testkeyp': 'Row1'})
print(test_table.get_item(Key={'testkeyp': 'Row1'})['Item'])
test_table.put_item(Item={'a': 2, 'b': 3, 'c': [1,2,3,4], 'testkeyp': 'Row1'})
print(test_table.get_item(Key={'testkeyp': 'Row1'})['Item'])
test_table.update_item(Key={'testkeyp': 'Row1'}, UpdateExpression='SET c = list_append(c, :i)', ExpressionAttributeValues={':i': [5,6,7,8]})
print(test_table.get_item(Key={'testkeyp': 'Row1'})['Item'])
