import Head from 'next/head'
import { getStore, getStoreProducts } from '../../api'
import { GetServerSideProps } from 'next'
import { Product, Store } from '../../types'
import { formatPrice } from '../../utils/numbers'
import { Badge, Box, Card, Container, HStack, Stack, Text, VStack } from '@chakra-ui/react'
import { partitionBy } from '../../utils/collections'
import Image from 'next/image'
import React, { RefObject, useEffect, useMemo, useState } from 'react'

type Props = {
  store: Store
  products: Product[]
}

export const getServerSideProps: GetServerSideProps<Props> = async (ctx) => {
  const storeId = ctx.query.id as string
  const store = await getStore(storeId)
  const products = await getStoreProducts(storeId)

  return {
    props: {
      store,
      products,
    },
  }
}

export default function StorePage({ store, products }: Props) {
  const groups = partitionBy(products, (p) => p.category)
  const categories = groups.map((g) => g.key)
  const selectedCategory = categories[0]
  const [focus, setFocus] = useState<string | null>(categories.length > 0 ? categories[0] : null)
  const categorySectionRefs = categories.map((category) => ({
    category,
    sectionRef: React.createRef<HTMLDivElement>(),
  }))

  React.useEffect(() => {
    const onEvent = () => {
      for (const { sectionRef, category } of categorySectionRefs) {
        const rect = sectionRef?.current?.getBoundingClientRect()
        const isInside = rect ? rect.top >= 0 && rect.top <= window.innerHeight : false

        if (isInside) {
          setFocus(category)
          return
        }
      }
    }
    document.addEventListener('scroll', onEvent)
    return () => document.removeEventListener('scroll', onEvent)
  }, [categorySectionRefs])

  console.log('focusedCategory', focus)

  return (
    <>
      <Head>
        <title>Landing Page</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main style={{ backgroundColor: '#fafafa', minHeight: '100vh' }}>
        <Stack margin={0} padding={1}>
          <Text fontWeight={'bold'} variant="subtitle1">
            {store.name}
          </Text>
        </Stack>
        <HStack
          align={'center'}
          bgColor={'#fafafa'}
          top={0}
          position={'sticky'}
          zIndex={10}
          py={2}
          overflowX={'scroll'}
          style={{ scrollbarWidth: 'none' }}
          borderBottom={'1px solid #e0e0e0'}
        >
          {categories.map((category, index) => (
            <Badge
              onClick={() =>
                categorySectionRefs
                  .find((ref) => ref.category === category)
                  ?.sectionRef.current?.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center',
                  })
              }
              ml={index === 0 ? 2 : 0}
              mr={index === categories.length - 1 ? 2 : 0}
              colorScheme="green"
              variant={focus === category ? 'solid' : 'subtle'}
              borderRadius={'md'}
              key={category}
              padding={1}
            >
              {category}
            </Badge>
          ))}
        </HStack>
        <Container>
          <Stack my={4} spacing={3}>
            {groups.map((group) => (
              <Stack
                ref={categorySectionRefs.find((ref) => ref.category === group.key)?.sectionRef}
                id={group.key}
                key={group.key}
              >
                <Stack
                  style={{ position: 'sticky', top: 0, backgroundColor: '#fafafa', zIndex: 1 }}
                  margin={0}
                >
                  <Text fontWeight={'bold'} variant="subtitle2">
                    {group.key}
                  </Text>
                </Stack>
                {group.items.map((product) => (
                  <Card key={product.id}>
                    <HStack p={2} alignItems={'flex-start'}>
                      <VStack
                        h={'100px'}
                        w={'100px'}
                        flexShrink={0}
                        borderRadius={'md'}
                        overflow={'hidden'}
                      >
                        <Image
                          quality={50}
                          src={'https://via.placeholder.com/150'}
                          width={100}
                          height={100}
                          alt={''}
                        />
                      </VStack>
                      <Stack margin={0} padding={2}>
                        <Stack spacing={1}>
                          <Text fontWeight={'bold'}>{product.name}</Text>
                          <Text fontSize="sm" color={'gray.500'} noOfLines={1}>
                            {product.description}
                          </Text>
                        </Stack>
                        <Text>{formatPrice(product.price)}</Text>
                      </Stack>
                    </HStack>
                  </Card>
                ))}
              </Stack>
            ))}
          </Stack>
        </Container>
      </main>
    </>
  )
}
